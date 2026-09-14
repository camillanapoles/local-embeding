# virtual-kubelet-saladcloud

- Virtual Kubelet provider oficial da Salad: **pods K8s rodam como SaladCloud container groups**.
- K8s padrão (inclusive KEDA) escala via API; o VK traduz para réplicas do container group.
- Padrão de uso: cluster no VPS/k3s agenda pod → executa em GPU Salad → mesmo `kubectl`, `Service`, escalonamento familiar.
