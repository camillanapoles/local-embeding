package com.local.embeding.ime

import org.json.JSONArray
import org.json.JSONObject

data class FsmStep(val id: String, val label: String, val template: String)

data class PromptFsm(
    val id: String, val name: String, val steps: List<FsmStep>,
    val intentAction: String?
) {
    fun render(template: String, vars: Map<String, String>): String {
        var t = template
        for ((k, v) in vars) t = t.replace("{{$k}}", v)
        return t
    }

    companion object {
        fun fromJson(s: String): PromptFsm {
            val o = JSONObject(s)
            val arr = o.optJSONArray("steps") ?: JSONArray()
            val steps = (0 until arr.length()).map {
                val st = arr.getJSONObject(it)
                FsmStep(st.optString("id", "s$it"), st.optString("label", "passo ${it + 1}"), st.getString("template"))
            }
            return PromptFsm(o.getString("id"), o.getString("name"), steps,
                o.optString("intent_action").ifEmpty { null })
        }
    }
}
