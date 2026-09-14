package com.local.embeding.ime

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast

import android.app.Activity
import kotlin.concurrent.thread

class MainActivity : Activity() {
    private lateinit var baseEt: EditText
    private lateinit var modelEt: EditText

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val dp = { v: Int -> (v * resources.displayMetrics.density).toInt() }
        val scroll = android.widget.ScrollView(this)
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL; setPadding(dp(16), dp(24), dp(16), dp(16))
        }
        root.addView(TextView(this).apply { text = "Local Embed Teclado — configuração"; textSize = 20f })
        root.addView(TextView(this).apply { text = "Endpoint (OpenAI-compat):"; textSize = 12f })
        baseEt = EditText(this).apply { setText(Prefs.base(this@MainActivity)); hint = "http://127.0.0.1:8080/v1" }
        root.addView(baseEt)
        root.addView(TextView(this).apply { text = "Modelo (id):"; textSize = 12f })
        modelEt = EditText(this).apply { setText(Prefs.model(this@MainActivity)); hint = "qwen3-1.7b" }
        root.addView(modelEt)
        val modeBtn = Button(this).apply { text = "saída do teclado: ${Prefs.mode(this@MainActivity)}" }
        modeBtn.setOnClickListener {
            val m = when (Prefs.mode(this)) { Prefs.MODE_TEXT -> Prefs.MODE_AUDIO; Prefs.MODE_AUDIO -> Prefs.MODE_BOTH; else -> Prefs.MODE_TEXT }
            Prefs.save(this, baseEt.text.toString().trim(), modelEt.text.toString().trim(), m)
            modeBtn.text = "saída do teclado: $m"
        }
        root.addView(modeBtn)
        root.addView(Button(this).apply {
            text = "Salvar"
            setOnClickListener {
                Prefs.save(this@MainActivity, baseEt.text.toString().trim(), modelEt.text.toString().trim(), Prefs.mode(this@MainActivity))
                toast("salvo")
            }
        })
        root.addView(Button(this).apply {
            text = "Testar endpoint"
            setOnClickListener {
                toast("testando…")
                thread {
                    val ok = LlmClient.health(baseEt.text.toString().trim())
                    runOnUiThread { toast(if (ok) "✅ endpoint respondeu" else "❌ sem resposta") }
                }
            }
        })
        root.addView(Button(this).apply {
            text = "Conceder permissão de microfone"
            setOnClickListener { requestPermissions(arrayOf(Manifest.permission.RECORD_AUDIO), 1) }
        })
        root.addView(TextView(this).apply {
            text = "Como usar: (1) rode o llama-server no Termux (ver README do repo); " +
                "(2) habilite este teclado em Ajustes ➞ Sistema ➞ Teclados; " +
                "(3) em qualquer campo de texto: 🎤 fala ou ▶ roda o prompt selecionado; " +
                "saída vai como texto digitado e/ou áudio conforme o modo. ⚡ dispara intents Android."
            textSize = 13f; setPadding(0, dp(16), 0, 0)
        })
        scroll.addView(root)
        setContentView(scroll)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        toast(if (grantResults.firstOrNull() == PackageManager.PERMISSION_GRANTED) "microfone ok" else "microfone negado")
    }

    private fun toast(s: String) = Toast.makeText(this, s, Toast.LENGTH_SHORT).show()
}
