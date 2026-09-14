package com.local.embeding.ime

import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object LlmClient {
    fun chat(baseUrl: String, model: String, prompt: String, timeoutMs: Int = 180000): String {
        val url = URL(baseUrl.trimEnd('/') + "/chat/completions")
        val conn = url.openConnection() as HttpURLConnection
        conn.requestMethod = "POST"
        conn.connectTimeout = 10000
        conn.readTimeout = timeoutMs
        conn.setRequestProperty("Content-Type", "application/json")
        val body = JSONObject().apply {
            put("model", model)
            put("stream", false)
            put("messages", JSONArray().put(JSONObject().put("role", "user").put("content", prompt)))
        }
        conn.outputStream.use { it.write(body.toString().toByteArray(Charsets.UTF_8)) }
        val code = conn.responseCode
        val text = (if (code in 200..299) conn.inputStream else conn.errorStream)
            ?.bufferedReader()?.use { it.readText() } ?: ""
        if (code !in 200..299) throw RuntimeException("HTTP $code: " + text.take(200))
        return JSONObject(text).getJSONArray("choices").getJSONObject(0)
            .getJSONObject("message").getString("content").trim()
    }

    fun health(baseUrl: String): Boolean = try {
        val conn = URL(baseUrl.trimEnd('/') + "/models").openConnection() as HttpURLConnection
        conn.connectTimeout = 3000; conn.readTimeout = 3000
        conn.responseCode in 200..299
    } catch (e: Exception) { false }
}
