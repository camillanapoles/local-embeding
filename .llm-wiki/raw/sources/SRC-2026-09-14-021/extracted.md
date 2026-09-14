# On-device LLM Android 2026

- Três caminhos dominantes: **llama.cpp** (C/C++, GGUF, JNI — SmolChat usa essa via), **MediaPipe LLM Inference** (Kotlin-first, modelos próprios, aceleração de hardware), **llama.rn** (React Native, .so + bindings, Hexagon NPU experimental, multimodal).
- Padrão RAG local: embeddings on-device (MiniLM/GGUF) + SQLite/FAISS ou Qdrant mobile + LLM via mesma cadeia JNI/MediaPipe.
- Decisão deste projeto: **APK cliente do endpoint OpenAI-compat** (llama-server no Termux, verificado) em vez de JNI embutido — CI builda APK sem NDK; JNI/SmolChat-style é débito planejado (TODO.md).
