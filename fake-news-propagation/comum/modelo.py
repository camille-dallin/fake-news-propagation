import random

IGNORANTE = 0
ESPALHADOR = 1
INATIVO = 2

def criargrade(linhas, colunas, percentualespalhadores=0.02, semente=42):
    random.seed(semente)
    grade = [[IGNORANTE for _ in range(colunas)] for _ in range(linhas)]
    totalcelulas = linhas * colunas
    totalespalhadores = int(totalcelulas * percentualespalhadores)
    posicoes = random.sample(range(totalcelulas), totalespalhadores)
    for pos in posicoes:
        i = pos // colunas
        j = pos % colunas
        grade[i][j] = ESPALHADOR
    return grade

def contarvizinhosespalhadores(grade, i, j):
    linhas = len(grade)
    colunas = len(grade[0])
    total = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = i + di
            nj = j + dj
            if 0 <= ni < linhas and 0 <= nj < colunas:
                if grade[ni][nj] == ESPALHADOR:
                    total += 1
    return total

def proximageracao(grade, limiarconvencimento=2):
    linhas = len(grade)
    colunas = len(grade[0])
    novagrade = [[IGNORANTE for _ in range(colunas)] for _ in range(linhas)]
    for i in range(linhas):
        for j in range(colunas):
            estadoatual = grade[i][j]
            if estadoatual == IGNORANTE:
                vizinhos = contarvizinhosespalhadores(grade, i, j)
                if vizinhos >= limiarconvencimento:
                    novagrade[i][j] = ESPALHADOR
                else:
                    novagrade[i][j] = IGNORANTE
            elif estadoatual == ESPALHADOR:
                novagrade[i][j] = INATIVO
            else:
                novagrade[i][j] = INATIVO
    return novagrade

def contarestados(grade):
    contagem = {IGNORANTE: 0, ESPALHADOR: 0, INATIVO: 0}
    for linha in grade:
        for celula in linha:
            contagem[celula] += 1
    return contagem

def gradeparatexto(grade):
    simbolos = {IGNORANTE: ".", ESPALHADOR: "E", INATIVO: "N"}
    linhastexto = []
    for linha in grade:
        linhastexto.append(" ".join(simbolos[celula] for celula in linha))
    return "\n".join(linhastexto)

def imprimirgrade(grade, limite=30):
    linhas = min(len(grade), limite)
    colunas = min(len(grade[0]), limite)
    simbolos = {IGNORANTE: ".", ESPALHADOR: "E", INATIVO: "N"}
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(simbolos[grade[i][j]])
        print(" ".join(linha))
    print()