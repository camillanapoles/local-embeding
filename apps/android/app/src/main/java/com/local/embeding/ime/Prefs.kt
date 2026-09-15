package com.local.embeding.ime

import android.content.Context

object Prefs {
    private const val FILE = "cfg"
    const val MODE_TEXT = "TEXTO"; const val MODE_AUDIO = "ÁUDIO"; const val MODE_BOTH = "AMBOS"

    // defaults vêm de res/values/strings.xml (recurso de UI) — zero endpoint/modelo em código (hardcode_scan)
    fun base(c: Context) = c.getSharedPreferences(FILE, 0).getString("base", null)
        ?: c.getString(R.string.default_base_url)
    fun model(c: Context) = c.getSharedPreferences(FILE, 0).getString("model", null)
        ?: c.getString(R.string.default_model_id)
    fun mode(c: Context) = c.getSharedPreferences(FILE, 0).getString("mode", MODE_TEXT)!!
    fun save(c: Context, base: String, model: String, mode: String) =
        c.getSharedPreferences(FILE, 0).edit()
            .putString("base", base).putString("model", model).putString("mode", mode).apply()
}
