# Latência do loop de voz (medições 2026)

- Pipeline streaming medido: LLM TTFT ~296ms + sentence detection ~143ms + TTS ~316ms = **TTFA ~755ms**.
- Alvo de barge-in 2026: **<150ms** p/ resposta a interrupção; turn-taking humano ≈ 200ms.
- Decomposição agressiva: VAD endpointing 200ms + STT final 100-150ms + TTS primeiro chunk 80ms ≈ ~400-520ms com transporte WebSocket.
- Maiores ganhos: **sentence-boundary streaming** (1ª frase → TTS imediato) e VAD Silero tunado (frames 30ms).
