import time
import threading

from comum.modelo import (
    criargrade,
    contarvizinhosespalhadores,
    contarestados,
    IGNORANTE,
    ESPALHADOR,
    INATIVO
)

class SimulacaoParalela:
    """
    Implementa a simulação paralela da propagação de fake news usando threads.
    Cada thread processa uma faixa exclusiva da matriz para evitar condições de corrida na escrita.
    Barreiras de sincronização são usadas para garantir a consistência entre as gerações.
    """
    def __init__(self, linhas, colunas, geracoes, percentual_espalhadores, limiar_convencimento, semente, num_threads):
        self.linhas = linhas
        self.colunas = colunas
        self.geracoes_maximas = geracoes
        self.limiar = limiar_convencimento
        self.num_threads = num_threads
        
        self.grade_atual = criargrade(linhas, colunas, percentual_espalhadores, semente)
        self.nova_grade = [[IGNORANTE for _ in range(colunas)] for _ in range(linhas)]
        
        self.geracoes_executadas = 0
        self.propagacao_ativa = True
        
        self.barreira_calculo = threading.Barrier(self.num_threads + 1)
        self.barreira_troca = threading.Barrier(self.num_threads + 1)

    def worker(self, id_thread, linha_inicio, linha_fim):
        """
        Função executada por cada thread worker.
        Calcula a próxima geração para sua faixa de linhas atribuída.
        Usa barreiras para sincronizar o cálculo e a troca de grades entre as gerações.
        """
        for _ in range(self.geracoes_maximas):
            if not self.propagacao_ativa:
                break
                
            for i in range(linha_inicio, linha_fim):
                for j in range(self.colunas):
                    estado = self.grade_atual[i][j]
                    
                    if estado == IGNORANTE:
                        vizinhos = contarvizinhosespalhadores(self.grade_atual, i, j)
                        if vizinhos >= self.limiar:
                            self.nova_grade[i][j] = ESPALHADOR
                        else:
                            self.nova_grade[i][j] = IGNORANTE
                    elif estado == ESPALHADOR:
                        self.nova_grade[i][j] = INATIVO
                    else:
                        self.nova_grade[i][j] = INATIVO
                        
            # Sincroniza o cálculo de todas as threads antes de avançar para a próxima geração
            # Isso garante que todas as threads terminaram de calcular seus respectivos pedaços da nova grade
            # antes que a grade seja trocada e a próxima geração comece.
            self.barreira_calculo.wait()
            self.barreira_troca.wait()

    def executar(self):
        """
        Inicia e coordena a execução da simulação paralela.
        Divide a matriz em faixas e atribui cada faixa a uma thread worker.
        Gerencia as barreiras de sincronização para o fluxo da simulação.
        """
        threads = []
        tamanho_faixa = self.linhas // self.num_threads
        resto = self.linhas % self.num_threads
        
        linha_atual = 0
        
        for i in range(self.num_threads):
            inicio = linha_atual
            fim = inicio + tamanho_faixa + (1 if i < resto else 0)
            linha_atual = fim
            
            t = threading.Thread(target=self.worker, args=(i, inicio, fim))
            threads.append(t)
            t.start()
            
        inicio_tempo = time.perf_counter()
        
        for geracao in range(self.geracoes_maximas):
            self.barreira_calculo.wait()
            
            # Troca as grades: a nova grade calculada se torna a grade atual para a próxima geração
            # Garante que todas as threads vejam a grade atualizada simultaneamente.
            self.geracoes_executadas += 1
            self.grade_atual, self.nova_grade = self.nova_grade, self.grade_atual
            
            contagem = contarestados(self.grade_atual)
            
            if contagem[ESPALHADOR] == 0:
                self.propagacao_ativa = False
                self.barreira_troca.wait()
                break
                
            # Se não houver mais espalhadores, a propagação para. Sinaliza às threads para terminarem.
            self.barreira_troca.wait()
            
        fim_tempo = time.perf_counter()
        tempo_total = fim_tempo - inicio_tempo
        
        # Aguarda todas as threads terminarem antes de retornar o tempo total.
        for t in threads:
            t.join()
            
        return tempo_total