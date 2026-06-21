import socket
import time
from comum.modelo import criargrade, contarestados, IGNORANTE, ESPALHADOR, INATIVO
from distribuido.protocolo import enviar_mensagem, receber_mensagem

def executar_mestre(linhas, colunas, geracoes, percentual, limiar, semente, num_workers, porta):
    grade = criargrade(linhas, colunas, percentual, semente)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', porta))
    server.listen(num_workers)

    print("=== SIMULACAO DISTRIBUIDA (MESTRE) ===")
    print(f"Aguardando {num_workers} workers conectarem na porta {porta}...")

    workers = []
    for _ in range(num_workers):
        conn, addr = server.accept()
        workers.append(conn)
    
    print("Todos os workers conectados!\n")

    contagem_inicial = contarestados(grade)
    print(f"Estado inicial -> Ignorantes: {contagem_inicial[IGNORANTE]} | Espalhadores: {contagem_inicial[ESPALHADOR]} | Inativos: {contagem_inicial[INATIVO]}\n")

    tamanho_faixa = linhas // num_workers
    resto = linhas % num_workers
    linha_atual = 0

    for i, conn in enumerate(workers):
        inicio = linha_atual
        fim = inicio + tamanho_faixa + (1 if i < resto else 0)
        linha_atual = fim
        
        subgrade = grade[inicio:fim]
        
        enviar_mensagem(conn, {
            "tipo": "INIT",
            "limiar": limiar,
            "colunas": colunas,
            "subgrade": subgrade
        })

    inicio_tempo = time.perf_counter()
    geracoes_executadas = 0

    for geracao in range(geracoes):
        fronteiras = []
        for conn in workers:
            msg = receber_mensagem(conn)
            fronteiras.append((msg["primeira_linha"], msg["ultima_linha"]))

        for i, conn in enumerate(workers):
            linha_cima = fronteiras[i-1][1] if i > 0 else None
            linha_baixo = fronteiras[i+1][0] if i < num_workers - 1 else None
            
            enviar_mensagem(conn, {
                "tipo": "BORDERS",
                "cima": linha_cima,
                "baixo": linha_baixo
            })

        total_ign = 0
        total_esp = 0
        total_ina = 0

        for conn in workers:
            msg = receber_mensagem(conn)
            total_ign += msg["ignorantes"]
            total_esp += msg["espalhadores"]
            total_ina += msg["inativos"]

        geracoes_executadas += 1
        print(f"Geracao {geracao + 1:03d} | Ignorantes: {total_ign:>6} | Espalhadores: {total_esp:>6} | Inativos: {total_ina:>6}")

        if total_esp == 0:
            print("\nA propagacao terminou: nao ha mais espalhadores.")
            break

    fim_tempo = time.perf_counter()
    tempo_total = fim_tempo - inicio_tempo

    for conn in workers:
        enviar_mensagem(conn, {"tipo": "FINISH"})
        conn.close()
    
    server.close()

    print("\n=== RESULTADO FINAL DISTRIBUIDO ===")
    print(f"Geracoes executadas: {geracoes_executadas}")
    print(f"Tempo total: {tempo_total:.6f} segundos")
    print(f"Ignorantes finais: {total_ign}")
    print(f"Espalhadores finais: {total_esp}")
    print(f"Inativos finais: {total_ina}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mestre para simulação distribuída de propagação de fake news.")
    parser.add_argument('--linhas', type=int, default=20, help='Número de linhas da grade.')
    parser.add_argument('--colunas', type=int, default=20, help='Número de colunas da grade.')
    parser.add_argument('--geracoes', type=int, default=10, help='Número de gerações a simular.')
    parser.add_argument('--percentual', type=float, default=0.05, help='Percentual inicial de espalhadores.')
    parser.add_argument('--limiar', type=int, default=3, help='Limiar de vizinhos para convencimento.')
    parser.add_argument('--semente', type=int, default=42, help='Semente para geração da grade inicial.')
    parser.add_argument('--num_workers', type=int, default=2, help='Número de workers esperados.')
    parser.add_argument('--porta', type=int, default=5000, help='Porta para comunicação com os workers.')
    args = parser.parse_args()
    executar_mestre(args.linhas, args.colunas, args.geracoes, args.percentual, args.limiar, args.semente, args.num_workers, args.porta)
    