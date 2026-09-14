# STT local 2026

- **Speaches** (ex-faster-whisper-server): API **OpenAI-compat `/v1/audio/transcriptions`**, streaming e live transcription; docker 1 comando; backends CPU/CUDA/Metal/Vulkan.
- faster-whisper = CTranslate2: 2-4× mais rápido que whisper de referência (int8/fp16).
- **whisper.cpp v1.8.x (2026)**: manutenção focada em **VAD streaming e estabilidade do server**; compila nativo em Termux/Android (mesmo toolchain do llama.cpp).
- Modelos: tiny/base p/ teste, **small** = equilíbrio tempo-real local, large-v3 = qualidade (GPU/paciência).
