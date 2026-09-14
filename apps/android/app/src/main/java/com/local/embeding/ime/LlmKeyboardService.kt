package com.local.embeding.ime

import android.content.Intent
import android.inputmethodservice.InputMethodService
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import org.json.JSONArray
import kotlin.concurrent.thread

class LlmKeyboardService : InputMethodService() {
    private var prompts: List<PromptFsm> = emptyList()
    private var current = 0
    private var mode = Prefs.MODE_TEXT
    private lateinit var status: TextView
    private lateinit var promptBtn: Button
    private lateinit var modeBtn: Button
    private val speaker by lazy { VoiceIO.Speaker(this) }

    override fun onCreate() {
        super.onCreate()
        prompts = loadPrompts()
    }

    private fun loadPrompts(): List<PromptFsm> {
        val out = mutableListOf<PromptFsm>()
        try {
            val files = assets.list("prompts") ?: emptyArray()
            for (f in files.sorted()) {
                if (f.endsWith(".json")) out += PromptFsm.fromJson(assets.open("prompts/$f").bufferedReader().readText())
            }
        } catch (e: Exception) { toast("prompts: ${e.message}") }
        if (out.isEmpty()) out += PromptFsm("raw", "Direto (sem prompt)", listOf(FsmStep("s1", "direto", "{{input}}")), null)
        return out
    }

    override fun onCreateInputView(): View {
        val ctx = this
        val dp = { v: Int -> (v * resources.displayMetrics.density).toInt() }
        val root = LinearLayout(ctx).apply {
            orientation = LinearLayout.VERTICAL; setPadding(dp(6), dp(6), dp(6), dp(6))
        }
        status = TextView(ctx).apply { text = "pronto"; textSize = 12f }
        promptBtn = Button(ctx).apply {
            text = prompts[current].name
            setOnClickListener {
                current = (current + 1) % prompts.size
                text = prompts[current].name
            }
        }
        modeBtn = Button(ctx).apply {
            text = "saída: $mode"
            setOnClickListener {
                mode = when (mode) { Prefs.MODE_TEXT -> Prefs.MODE_AUDIO; Prefs.MODE_AUDIO -> Prefs.MODE_BOTH; else -> Prefs.MODE_TEXT }
                Prefs.save(ctx, Prefs.base(ctx), Prefs.model(ctx), mode)
                text = "saída: $mode"
            }
        }
        val voiceBtn = Button(ctx).apply { text = "🎤 falar" }
        val runBtn = Button(ctx).apply { text = "▶ rodar prompt" }
        val actionBtn = Button(ctx).apply { text = "⚡ ação"; visibility = if (prompts[current].intentAction != null) View.VISIBLE else View.GONE }
        val row = LinearLayout(ctx).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL }
        listOf<Button>(voiceBtn, runBtn, actionBtn).forEach {
            row.addView(it, LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f))
        }

        voiceBtn.setOnClickListener {
            val perm = android.content.pm.PackageManager.PERMISSION_GRANTED ==
                this@LlmKeyboardService.checkSelfPermission(android.Manifest.permission.RECORD_AUDIO)
            if (!perm) { toast("conceda o microfone no app Local Embed"); return@setOnClickListener }
            status.text = "ouvindo…"
            VoiceIO.listen(ctx, { saida -> currentInputConnection?.commitText(saida + " ", 1); status.text = "ok" },
                { e -> status.text = e })
        }
        runBtn.setOnClickListener { runPrompt(readInput()) }
        promptBtn.setOnClickListener {
            current = (current + 1) % prompts.size  // garantido tb no setOnClickListener acima
            actionBtn.visibility = if (prompts[current].intentAction != null) View.VISIBLE else View.GONE
        }
        actionBtn.setOnClickListener { runAction(readInput()) }

        root.addView(status)
        root.addView(promptBtn)
        root.addView(modeBtn)
        root.addView(row)
        return root
    }

    private fun readInput(): String {
        val ic = currentInputConnection ?: return ""
        val cur = ic.getTextBeforeCursor(4000, 0).toString() + ic.getTextAfterCursor(4000, 0).toString()
        return cur.trim()
    }

    private fun runPrompt(input: String) {
        if (input.isBlank()) { toast("digite/fale algo primeiro"); return }
        val fsm = prompts[current]
        val base = Prefs.base(this); val model = Prefs.model(this)
        status.text = "⏳ ${fsm.name}…"
        thread {
            try {
                var prev = ""
                var out = ""
                for (step in fsm.steps) {
                    val prompt = fsm.render(step.template, mapOf("input" to input, "prev" to prev))
                    out = LlmClient.chat(base, model, prompt)
                    prev = out
                }
                Handler(Looper.getMainLooper()).post {
                    status.text = "✓ pronto"
                    if (mode != Prefs.MODE_AUDIO) currentInputConnection?.commitText(out + "\n", 1)
                    if (mode != Prefs.MODE_TEXT) speaker.speak(out)
                }
            } catch (e: Exception) {
                Handler(Looper.getMainLooper()).post { status.text = "erro: ${e.message?.take(80)}" }
            }
        }
    }

    private fun runAction(input: String) {
        val fsm = prompts[current]
        val action = fsm.intentAction ?: return
        val base = Prefs.base(this); val model = Prefs.model(this)
        status.text = "⏳ ação…"
        thread {
            try {
                var prev = ""; var out = input
                for (step in fsm.steps) {
                    out = LlmClient.chat(base, model, fsm.render(step.template, mapOf("input" to input, "prev" to prev)))
                    prev = out
                }
                val finalText = out
                Handler(Looper.getMainLooper()).post {
                    status.text = "✓ disparando intent"
                    val i = Intent(action).apply {
                        putExtra(Intent.EXTRA_TEXT, finalText)
                        type = "text/plain"
                        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    }
                    try { startActivity(i) } catch (e: Exception) { toast("intent falhou: ${e.message}") }
                }
            } catch (e: Exception) {
                Handler(Looper.getMainLooper()).post { status.text = "erro: ${e.message?.take(80)}" }
            }
        }
    }

    private fun toast(s: String) = Toast.makeText(this, s, Toast.LENGTH_SHORT).show()
}
