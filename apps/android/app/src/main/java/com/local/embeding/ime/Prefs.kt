package com.local.embeding.ime

import android.content.Context

object Prefs {
    private const val FILE = "cfg"
    const val DEFAULT_BASE = "http://127.0.0.1:8080/v1"
    const val DEFAULT_MODEL = "qwen3-1.7b"
    const val MODE_TEXT = "TEXTO"; const val MODE_AUDIO = "ÁUDIO"; const val MODE_BOTH = "AMBOS"

    fun base(c: Context) = c.getSharedPreferences(FILE, 0).getString("base", DEFAULT_BASE)!!
    fun model(c: Context) = c.getSharedPreferences(FILE, 0).getString("model", DEFAULT_MODEL)!!
    fun mode(c: Context) = c.getSharedPreferences(FILE, 0).getString("mode", MODE_TEXT)!!
    fun save(c: Context, base: String, model: String, mode: String) =
        c.getSharedPreferences(FILE, 0).edit()
            .putString("base", base).putString("model", model).putString("mode", mode).apply()
}
