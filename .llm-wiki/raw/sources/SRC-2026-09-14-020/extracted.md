# Vocabulário custom no Whisper (sem fine-tuning)

- `initial_prompt` (a.k.a. `prompt`): insere os termos desejados no início do contexto de decodificação → eleva log-probabilidade desses tokens ao longo da transcrição. Funciona como "glossário leve" (OpenAI Cookbook; HF Forums; contextual biasing — arXiv 2410.18363).
- faster-whisper aceita `initial_prompt` e `hotwords`; whisper.cpp server aceita `prompt` no multipart `/inference`.
- Boas práticas: prompt curto (~200 tokens), em frase natural, com siglas/grafias exatas; combinar com `suppress_tokens` p/ bloquear alternativas indesejadas.
- Uso típico relatado: nomes próprios, jargão de domínio, nomes de produto — exatamente o caso de jargão EN de engenharia de software em fala PT-BR.
