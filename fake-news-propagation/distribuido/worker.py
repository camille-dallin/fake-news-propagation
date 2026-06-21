import socket
from comum.modelo import IGNORANTE, ESPALHADOR, INATIVO
from distribuido.protocolo import enviar_mensagem, receber_mensagem

def contar_vizinhos_worker(grade_local, fantasma_cima, fantasma_baixo, i, j, colunas):
    linhas = len(grade_local)
    total = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= nj < colunas:
                if ni == -1 and fantasma_cima and fantasma_cima[nj] == ESPALHADOR:
                    total += 1
                elif ni == linhas and fantasma_baixo and fantasma_baixo[nj] == ESPALHADOR:
                    total += 1
                elif 0 <= ni < linhas and grade_local[ni][nj] == ESPALHADOR:
                    total += 1
    return total

def executar_worker(host='localhost', porta=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, porta))
    except ConnectionRefusedError:
        print("Erro: Nao encontrei o mestre. Rode o mestre.py primeiro!")
        return

    msg_init = receber_mensagem(sock)
    if not msg_init:
        return

    subgrade = msg_init["subgrade"]
    limiar = msg_init["limiar"]
    colunas = msg_init["colunas"]

    try:
        while True:
            enviar_mensagem(sock, {
                "tipo": "BOUNDARIES",
                "primeira_linha": subgrade[0],
                "ultima_linha": subgrade[-1]
            })

            msg_mestre = receber_mensagem(sock)
            
            if not msg_mestre or msg_mestre.get("tipo") == "FINISH":
                break

            fantasma_cima = msg_mestre["cima"]
            fantasma_baixo = msg_mestre["baixo"]

            nova_subgrade = [[IGNORANTE for _ in range(colunas)] for _ in range(len(subgrade))]
            ign, esp, ina = 0, 0, 0

            for i in range(len(subgrade)):
                for j in range(colunas):
                    estado = subgrade[i][j]
                    if estado == IGNORANTE:
                        vizinhos = contar_vizinhos_worker(subgrade, fantasma_cima, fantasma_baixo, i, j, colunas)
                        if vizinhos >= limiar:
                            nova_subgrade[i][j] = ESPALHADOR
                        else:
                            nova_subgrade[i][j] = IGNORANTE
                    elif estado == ESPALHADOR:
                        nova_subgrade[i][j] = INATIVO
                    else:
                        nova_subgrade[i][j] = INATIVO

                    novo_estado = nova_subgrade[i][j]
                    if novo_estado == IGNORANTE: ign += 1
                    elif novo_estado == ESPALHADOR: esp += 1
                    else: ina += 1

            subgrade = nova_subgrade

            enviar_mensagem(sock, {
                "tipo": "STEPRESULT",
                "ignorantes": ign,
                "espalhadores": esp,
                "inativos": ina
            })
    except ConnectionResetError:
        pass
    finally:
        sock.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Worker para simulação distribuída de propagação de fake news.")
    parser.add_argument('--host', type=str, default='localhost', help='Host do mestre.')
    parser.add_argument('--porta', type=int, default=5000, help='Porta do mestre.')
    args = parser.parse_args()
    executar_worker(args.host, args.porta)