import time

from comum.modelo import (
    criargrade,
    proximageracao,
    contarestados,
    IGNORANTE,
    ESPALHADOR,
    INATIVO
)

def executarsimulacaosequencial(
    linhas=100,
    colunas=100,
    geracoes=50,
    percentualespalhadores=0.05,
    limiarconvencimento=3,
    semente=42,
    mostrargrade=False
):
    grade = criargrade(
        linhas=linhas,
        colunas=colunas,
        percentualespalhadores=percentualespalhadores,
        semente=semente
    )

    inicio = time.perf_counter()
    geracoesexecutadas = 0

    for geracao in range(geracoes):
        grade = proximageracao(grade, limiarconvencimento)
        geracoesexecutadas += 1

        contagem = contarestados(grade)

        if contagem[ESPALHADOR] == 0:
            break

    fim = time.perf_counter()
    tempototal = fim - inicio

    contagemfinal = contarestados(grade)

    return {
        "tempototal": tempototal,
        "geracoesexecutadas": geracoesexecutadas,
        "contagemfinal": contagemfinal,
        "gradefinal": grade
    }

if __name__ == "__main__":
    resultado = executarsimulacaosequencial(
        linhas=20,
        colunas=20,
        geracoes=10,
        percentualespalhadores=0.05,
        limiarconvencimento=3,
        semente=42,
        mostrargrade=False
    )
    print(f"Tempo: {resultado['tempototal']}s")