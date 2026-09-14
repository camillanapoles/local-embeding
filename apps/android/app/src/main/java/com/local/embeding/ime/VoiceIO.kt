package com.local.embeding.ime

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import java.util.Locale

object VoiceIO {
    fun listen(context: Context, onResult: (String) -> Unit, onError: (String) -> Unit) {
        if (!SpeechRecognizer.isRecognitionAvailable(context)) {
            onError("reconhecimento de voz indisponível"); return
        }
        val sr = SpeechRecognizer.createSpeechRecognizer(context)
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR")
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
        }
        sr.setRecognitionListener(object : RecognitionListener {
            override fun onResults(r: Bundle) {
                val txt = r.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)?.firstOrNull() ?: ""
                sr.destroy(); if (txt.isBlank()) onError("nada reconhecido") else onResult(txt)
            }
            override fun onError(e: Int) { sr.destroy(); onError("erro STT $e") }
            override fun onPartialResults(partialResults: Bundle?) {}
            override fun onReadyForSpeech(p: Bundle?) {}
            override fun onBeginningOfSpeech() {}
            override fun onRmsChanged(r: Float) {}
            override fun onBufferReceived(b: ByteArray?) {}
            override fun onEndOfSpeech() {}
            override fun onEvent(i: Int, b: Bundle?) {}
        })
        sr.startListening(intent)
    }

    class Speaker(context: Context) {
        private var ready = false
        private val tts = TextToSpeech(context) { ready = it == TextToSpeech.SUCCESS }
        fun speak(text: String) {
            if (ready) tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "le1")
        }
        fun shutdown() { tts.stop(); tts.shutdown() }
    }
}
