# IME com voz e LLM — padrões 2026

- whisper-to-input: teclado Android que faz STT (Whisper) e insere o texto — valida o padrão IME+voz.
- Stack de referência 2026: SpeechRecognizer (baseline) → LLM local (Phi-4-mini/Gemma/Qwen quantizados) → function-calling → **Intent/App Action** (abrir apps, enviar, shortcuts).
- Este projeto adiciona: **prompts FSM** (steps com {{input}}/{{prev}}) e **saída selecionável** (texto no campo via InputConnection / TTS / ambos) + intent ACTION_SEND no prompt intent-action.
