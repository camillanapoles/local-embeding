# SaladCloud — Container Groups & Gateway

- Container Group = imagem + requisitos de hardware + replica count.
- **Container Gateway**: expõe o grupo na internet — porta configurável (80/custom), **API-key auth opcional por request**, URL estática com load-balance entre réplicas, IPv4 e IPv6.
- Réplicas ajustáveis a qualquer momento (escala manual/API).
- Storage é **efêmero** → workloads stateless (embedding server é o caso ideal).
- "Secure GPU Clusters" (datacenter) para quem não aceita nós comunitários.
- Docs de performance: dezenas a milhares de GPUs p/ inferência on-demand com load balancer.
