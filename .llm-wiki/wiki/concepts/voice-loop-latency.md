---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-017]
---

# Loop de voz e latência (fluidez)

Conversa fluida = pipeline, não modelo: VAD➞STT➞LLM➞TTS com streaming em cada fronteira.

## Como funciona

- **VAD Silero** agressivo: frames 30ms, endpointing ~200ms; **barge-in <150ms** (cortar TTS quando usuário fala).
- **STT streaming**: parciais ~150ms (opcional alimentar LLM antes do final).
- **Sentence-boundary streaming**: 1ª frase completa do LLM ➞ TTS imediato; não esperar resposta inteira (maior ganho único).
- **Echo cancellation** no cliente (senão o TTS dispara o VAD).
- Medições 2026: TTFA ~755ms end-to-end; ~400-520ms com WebSocket e pipeline afinado. Phone local: 1-2s realista.

## Exemplos

- Termux: whisper.cpp + Piper + LLM local (half-duplex tolerável)
- VPS hub: Speaches + Kokoro + LLM, phone = cliente fino (captura/playback)

Relacionados: [whisper.cpp](/entities/whisper-cpp.md) · [Speaches](/entities/speaches.md) · [Kokoro](/entities/kokoro.md) · [endpoint OpenAI-compat](/concepts/openai-compat-embedding-endpoint.md)
