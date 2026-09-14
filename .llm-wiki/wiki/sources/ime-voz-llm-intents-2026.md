---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-022/extracted.md
ingested: 2026-09-14
topics: [android-stack, voice-stack]
tier: A
---

# IME + voz + LLM + intents — padrão 2026

> _Original: [whisper-to-input](https://github.com/j3soon/whisper-to-input) · [Picovoice](https://picovoice.ai/blog/ai-voice-assistant-for-android-powered-by-local-llm) · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-022]]_

## Resumo

whisper-to-input valida teclado-IME-com-STT; stack 2026: SpeechRecognizer → LLM local → function-calling → Intents/App Actions. Este repo adiciona prompts FSM + saída selecionável (texto/áudio/ambos).

## Key Takeaways

- IME é o ponto de integração universal (funciona em qualquer app)
- Intents Android são o "tool use" do teclado

## Conceitos Mencionados

- [Loop de voz](/concepts/voice-loop-latency.md)

## Fonte

- [SRC-2026-09-14-022/extracted.md](../../raw/sources/SRC-2026-09-14-022/extracted.md)
