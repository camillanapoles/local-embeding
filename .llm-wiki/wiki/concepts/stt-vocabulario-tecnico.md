---
type: concept
domain: ai
created: 2026-09-14
updated: 2026-09-14
sources: [raw/sources/SRC-2026-09-14-020]
---

# STT com vocabulário técnico (PT-BR + jargão EN)

Falar PT misturado com termos técnicos EN sem que o STT invente grafia (*disploy, imbeding*).

## Como aplicar

1. **initial_prompt/hotwords**: glossário curto em frase natural condiciona a decodificação (whisper.cpp: campo `prompt` em `/inference`; faster-whisper: `initial_prompt`+`hotwords`).
2. **Pós-correção fuzzy**: dicionário `EN | forma falada BR | categoria` aplicado na saída antes do LLM.
3. Artefato do projeto: `tools/glossario-tech-ptbr.txt` (PROMPT_PRONTO ~180 tokens + ~120 entradas, incl. aportuguesadas reais: deployar, commitar, mergear, cachear).

Relacionados: [whisper.cpp](/entities/whisper-cpp.md) · [loop de voz](/concepts/voice-loop-latency.md) · [fonte whisper-vocab](/sources/whisper-vocabulario-custom.md)
