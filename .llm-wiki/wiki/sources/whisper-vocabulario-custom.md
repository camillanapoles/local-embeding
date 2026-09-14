---
type: source
format: article
raw_path: .llm-wiki/raw/sources/SRC-2026-09-14-020/extracted.md
ingested: 2026-09-14
topics: [voice-stack]
tier: A
---

# Whisper — vocabulário custom (initial_prompt/hotwords)

> _Original: [OpenAI Cookbook](https://developers.openai.com/cookbook/examples/whisper_prompting_guide) · [HF Forums](https://discuss.huggingface.co/t/adding-custom-vocabularies-on-whisper/29311) · arXiv 2410.18363 · Verificação: snippet · Packet: [[sources/SRC-2026-09-14-020]]_

## Resumo

`initial_prompt` condiciona a decodificação do Whisper elevando a probabilidade de tokens do glossário — sem fine-tuning. faster-whisper: `initial_prompt` + `hotwords`; whisper.cpp server: campo `prompt` em `/inference`.

## Key Takeaways

- Prompt curto (~200 tokens) em frase natural com siglas/grafias exatas
- Combina com `suppress_tokens`
- Caso de uso: jargão EN (deploy, endpoint, merge) dentro de fala PT-BR — aplicado em `tools/glossario-tech-ptbr.txt`

## Entidades Mencionadas

- [whisper.cpp](/entities/whisper-cpp.md) · [Speaches](/entities/speaches.md)

## Conceitos Mencionados

- [STT vocabulário técnico](/concepts/stt-vocabulario-tecnico.md)

## Fonte

- [SRC-2026-09-14-020/extracted.md](../../raw/sources/SRC-2026-09-14-020/extracted.md)
