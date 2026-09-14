# llama.cpp — docs/android.md

Repo oficial, documento vivo (2026).

- Termux = ambiente Linux/Android **sem root** — build nativo suportado.
- Toolchain Termux: `pkg install git clang cmake ninja python libandroid-spawn wget unzip`.
- Build nativo (sem NDK) no Termux: `cmake -B build && cmake --build build -j`.
- Caminho NDK (`-DCMAKE_TOOLCHAIN_FILE=$NDK/... -DANDROID_ABI=arm64-v8a`) existe para builds de APK.
- `llama-server` expõe API OpenAI-compat incluindo `/v1/embeddings` com `--embedding`.
- Tutorial correlato (algorist.co.uk, 2026-06-08): `llama-server` no Android via ssh/Termux (porta 8022) + tmux.
