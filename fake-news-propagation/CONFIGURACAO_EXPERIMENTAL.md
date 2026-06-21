# ⚙️ Configuração Experimental

Este documento detalha o ambiente de hardware e software utilizado para a execução dos experimentos de simulação de propagação de fake news nas versões sequencial, paralela e distribuída.

## 💻 Ambiente de Hardware

| Componente    | Detalhes                                    |
| :------------ | :------------------------------------------ |
| Processador   | Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz |
| Núcleos       | 2 vCPU                                      |
| Memória RAM   | 8 GB                                        |

## 🖥️ Ambiente de Software

| Componente            | Detalhes                                    |
| :-------------------- | :------------------------------------------ |
| Sistema Operacional   | Ubuntu 24.04 LTS (Linux/amd64)              |
| Linguagem de Programação | Python                                      |
| Versão do Interpretador | Python 3.11.0rc1                            |
| Bibliotecas Python    | `pandas`, `matplotlib` (instaladas via `pip`) |

## ☁️ Ambiente de Execução

Os experimentos foram executados em ambiente Linux (container/VM isolada), garantindo consistência na execução e na medição de desempenho entre as diferentes rodadas. A comunicação entre o mestre e os workers na versão distribuída foi realizada via sockets TCP na interface de loopback (`localhost`).

**Observação:** A execução em máquina virtual/container pode introduzir uma pequena sobrecarga de desempenho em comparação com hardware físico dedicado. Ainda assim, para fins de comparação *relativa* entre as versões sequencial, paralela e distribuída — que é o objetivo central da análise de speedup e eficiência —, o ambiente utilizado oferece controle e reprodutibilidade adequados, já que todas as versões foram medidas nas mesmas condições.
