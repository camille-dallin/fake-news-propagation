import time
import random
from comum.modelo import (
    criargrade, 
    contarvizinhosespalhadores, 
    contarestados, 
    IGNORANTE, 
    ESPALHADOR, 
    INATIVO
)

def proximageracao_probabilistica(grade, alfa=0.35):
    linhas = len(grade)
    colunas = len(grade[0])
    novagrade = [[IGNORANTE for _ in range(colunas)] for _ in range(linhas)]
    
    for i in range(linhas):
        for j in range(colunas):
            estadoatual = grade[i][j]
            
            if estadoatual == IGNORANTE:
                vizinhos = contarvizinhosespalhadores(grade, i, j)
                chance = min(1.0, alfa * vizinhos)
                
                if random.random() < chance:
                    novagrade[i][j] = ESPALHADOR
                else:
                    novagrade[i][j] = IGNORANTE
                    
            elif estadoatual == ESPALHADOR:
                novagrade[i][j] = INATIVO
            else:
                novagrade[i][j] = INATIVO
                
    return novagrade

def executar_melhoria():
    print("=== SIMULACAO EXTRA: PROBABILIDADE DE CONVENCIMENTO ===")
    alfa_teste = 0.35 
    print(f"Cada vizinho espalhador adiciona {alfa_teste * 100}% de chance de convencimento.\n")
    
    grade = criargrade(linhas=20, colunas=20, percentualespalhadores=0.05, semente=42)
    contagem_inicial = contarestados(grade)
    
    print(f"Estado inicial -> Ignorantes: {contagem_inicial[IGNORANTE]} | Espalhadores: {contagem_inicial[ESPALHADOR]} | Inativos: {contagem_inicial[INATIVO]}\n")
    
    for geracao in range(15):
        grade = proximageracao_probabilistica(grade, alfa=alfa_teste)
        contagem = contarestados(grade)
        
        print(f"Geracao {geracao + 1:03d} | Ignorantes: {contagem[IGNORANTE]:>6} | Espalhadores: {contagem[ESPALHADOR]:>6} | Inativos: {contagem[INATIVO]:>6}")
        
        if contagem[ESPALHADOR] == 0:
            print("\nA propagacao terminou: nao ha mais espalhadores.")
            break

if __name__ == "__main__":
    executar_melhoria()