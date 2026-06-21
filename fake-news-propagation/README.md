# 🦠 Simulação de Propagação de Fake News

Este projeto implementa uma simulação da propagação de *Fake News* utilizando o modelo de **Autômatos Celulares** (com Vizinhança de Moore). O objetivo é analisar o ganho de desempenho (*Speedup* e Eficiência) ao dividir o processamento em arquiteturas paralelas e distribuídas.

## ⚙️ Estrutura do Projeto

O projeto foi dividido em três abordagens principais para comparação de desempenho, além de uma melhoria extra:

1. **Versão Sequencial:** A base lógica e de comportamento do modelo.
2. **Versão Paralela:** Particionamento da matriz por faixas horizontais utilizando *Threads* e barreira de sincronização para evitar condição de corrida.
3. **Versão Distribuída:** Arquitetura Mestre-Worker utilizando Sockets TCP. A matriz é distribuída pela rede com troca de "linhas fantasmas" (fronteiras) a cada geração.
4. **Melhoria Extra (Modelo Probabilístico):** Uma versão estocástica onde o convencimento não é determinístico, mas baseado em uma probabilidade de acordo com o número de vizinhos.

## 🚀 Requisitos

* Python 3.11 ou superior (Testado na versão 3.11.0rc1)
* Bibliotecas: pandas, matplotlib

Para instalar as dependências necessárias, execute no terminal:
pip install pandas matplotlib

## 🎮 Como Executar

### 1. Versão Sequencial
Executa a simulação base em uma única thread:
python -m sequencial.simulacao_sequencial

### 2. Versão Paralela (Threads)
Executa a simulação dividindo o trabalho entre múltiplas threads locais:
python -m paralelo.simulacao_paralela

### 3. Versão Distribuída (Sockets)
Para rodar a versão distribuída, a execução é orquestrada pelo script de experimentos, que inicia o mestre e os workers automaticamente. **Para executar em máquinas diferentes, altere o parâmetro `--host` no `worker.py` para o IP do mestre.**

### 4. Automatização e Gráficos (Benchmark)
Para rodar a bateria de testes automatizados, que inclui as versões sequencial, paralela e distribuída, e gerar os gráficos de desempenho (Speedup, Eficiência e Tempos de Execução):

```bash
python -m experimentos.executar_experimentos
python -m experimentos.gerar_graficos
```

Os resultados detalhados serão salvos em `experimentos/resultados.csv` e os gráficos em `experimentos/grafico_speedup.png`, `experimentos/grafico_eficiencia.png` e `experimentos/grafico_tempos.png`.

Os gráficos serão salvos na pasta `experimentos`.

### 5. Simulação Probabilística (Ponto Extra)
Para executar o modelo avançado com probabilidade de convencimento estocástica:
python -m sequencial.simulacao_probabilistica

## 📊 Resultados e Conclusões
* **Paralelismo em Python:** Devido ao impacto do GIL (*Global Interpreter Lock*), o ganho de desempenho (*speedup*) em tarefas restritas à CPU cresce até certo ponto, mas a eficiência diminui à medida que mais threads são adicionadas.
* **Sistema Distribuído:** A divisão por particionamento de dados exigiu a troca das linhas de fronteira a cada geração. Embora exista sobrecarga (*overhead*) de rede, a arquitetura manteve 100% da integridade da Vizinhança de Moore distribuída.
## 📚 Referências Bibliográficas

[1] WOLFRAM, S. *A New Kind of Science*. Champaign: Wolfram Media, 2002. ISBN 978-1579550080.

[2] VON NEUMANN, J. *Theory of Self-Reproducing Automata*. Edited and completed by Arthur W. Burks. Urbana: University of Illinois Press, 1966.

[3] CHOPARD, B.; DROZ, M. *Cellular Automata Modeling of Physical Systems*. Cambridge: Cambridge University Press, 1998. ISBN 978-0521461683.

[4] EASLEY, D.; KLEINBERG, J. *Networks, Crowds, and Markets: Reasoning About a Highly Connected World*. Cambridge: Cambridge University Press, 2010. Disponível em: https://www.cs.cornell.edu/home/kleinber/networks-book/ — capítulo 19 trata especificamente de modelos de propagação de informação/contágio em redes.

[5] KERMACK, W. O.; McKENDRICK, A. G. A Contribution to the Mathematical Theory of Epidemics. *Proceedings of the Royal Society A*, v. 115, n. 772, p. 700–721, 1927. DOI: 10.1098/rspa.1927.0118 — base matemática clássica para modelos de propagação (estados tipo Susceptível-Infectado-Removido, análogos a Ignorante-Espalhador-Inativo usados neste trabalho).

[6] VOSOUGHI, S.; ROY, D.; ARAL, S. The spread of true and false news online. *Science*, v. 359, n. 6380, p. 1146–1151, 2018. DOI: 10.1126/science.aap9559 — estudo empírico sobre propagação de fake news em redes sociais, motivação real-world para o modelo implementado.

[7] PYTHON SOFTWARE FOUNDATION. *threading — Thread-based parallelism*. Python 3.11 Documentation. Disponível em: https://docs.python.org/3.11/library/threading.html — referência técnica para `threading.Thread` e `threading.Barrier`, usados na versão paralela.

[8] PYTHON SOFTWARE FOUNDATION. *socket — Low-level networking interface*. Python 3.11 Documentation. Disponível em: https://docs.python.org/3.11/library/socket.html — referência técnica para a comunicação via Sockets TCP na versão distribuída.

[9] TANENBAUM, A. S.; VAN STEEN, M. *Distributed Systems: Principles and Paradigms*. 2. ed. Upper Saddle River: Prentice Hall, 2007. ISBN 978-0132392273 — fundamentação teórica da arquitetura mestre-worker e sincronização de fronteiras (ghost rows) utilizada na versão distribuída.

[10] BEAZLEY, D. M. Understanding the Python GIL. In: *PyCon US*, 2010. Disponível em: https://dabeaz.com/python/UnderstandingGIL.pdf — referência técnica usada para justificar o comportamento de speedup sub-linear observado na versão paralela (impacto do Global Interpreter Lock).

## 📝 Notas de Implementação e Justificativas

### Condição de Corrida (Race Condition) na Versão Paralela

A condição de corrida foi evitada na implementação paralela (`paralelo/simulacao_paralela.py`) através de duas estratégias principais:

1.  **Particionamento Exclusivo da Matriz:** Cada thread worker é responsável por calcular e atualizar uma faixa exclusiva de linhas da matriz `nova_grade`. Isso garante que não haja escrita concorrente na mesma posição da matriz por diferentes threads, eliminando a possibilidade de *race conditions* na fase de cálculo.
2.  **Sincronização por Barreiras (`threading.Barrier`):** Duas barreiras são utilizadas para sincronizar o fluxo de execução entre as gerações:
    *   `barreira_calculo`: Garante que todas as threads concluam o cálculo de suas respectivas faixas da `nova_grade` antes que a grade `grade_atual` seja trocada. Isso assegura que todas as threads utilizem dados consistentes da geração anterior para o cálculo da próxima.
    *   `barreira_troca`: Após a troca das grades (onde `nova_grade` se torna `grade_atual`), esta barreira garante que todas as threads estejam prontas para iniciar o cálculo da próxima geração com a grade atualizada. Em caso de parada antecipada da simulação (quando não há mais espalhadores), esta barreira também é utilizada para sinalizar o término às threads workers.

Essa abordagem garante a integridade dos dados e a consistência da simulação entre as gerações, mesmo em um ambiente multi-threaded.

### Sincronização das Fronteiras na Versão Distribuída (Ghost Rows)

Na versão distribuída, a sincronização das fronteiras da matriz entre os processos (mestre e workers) é realizada utilizando o conceito de "linhas fantasmas" (*ghost rows*). Cada worker recebe uma sub-grade da matriz principal e, a cada geração, troca as linhas de fronteira com seus vizinhos adjacentes (worker acima e worker abaixo).

*   **Envio de Fronteiras:** Antes de cada nova geração, cada worker envia sua primeira e última linha (que servem como fronteiras) para o processo mestre.
*   **Distribuição de Fronteiras:** O mestre coleta essas linhas de fronteira de todos os workers e as retransmite para os workers vizinhos apropriados. Por exemplo, a última linha do worker `i` é enviada como `linha_cima` para o worker `i+1`, e a primeira linha do worker `i+1` é enviada como `linha_baixo` para o worker `i`.
*   **Cálculo com Linhas Fantasmas:** Os workers utilizam essas "linhas fantasmas" recebidas para calcular corretamente o estado dos indivíduos em suas próprias fronteiras, sem a necessidade de reconstruir a matriz global no mestre a cada iteração. Isso reduz a sobrecarga de comunicação e mantém a consistência da vizinhança de Moore em todo o sistema distribuído.

Essa técnica é fundamental para manter a integridade do modelo de autômatos celulares em um ambiente distribuído, onde cada processo opera apenas em uma porção da matriz global.
