
import subprocess
import time
import os
import sys

def executar_distribuido(linhas, colunas, geracoes, percentual, limiar, semente, num_workers, porta):
    # Comando para iniciar o mestre
    cmd_mestre = [sys.executable, '-m', 'distribuido.mestre', '--linhas', str(linhas), '--colunas', str(colunas), '--geracoes', str(geracoes), '--percentual', str(percentual), '--limiar', str(limiar), '--semente', str(semente), '--num_workers', str(num_workers), '--porta', str(porta)]
    
    # Inicia o mestre em um processo separado
    processo_mestre = subprocess.Popen(cmd_mestre, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(1) # Dá um tempo para o mestre iniciar e abrir a porta

    processos_workers = []
    for _ in range(num_workers):
        cmd_worker = [sys.executable, '-m', 'distribuido.worker', '--host', 'localhost', '--porta', str(porta)]
        processos_workers.append(subprocess.Popen(cmd_worker, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))

    # Espera o mestre terminar (ele controla a simulação)
    stdout_mestre, stderr_mestre = processo_mestre.communicate()

    # Coleta a saída dos workers (pode ser útil para depuração, mas não é estritamente necessário para o tempo)
    for p_worker in processos_workers:
        p_worker.communicate()

    # Extrai o tempo total do output do mestre
    tempo_total = 0.0
    for line in stdout_mestre.splitlines():
        if "Tempo total:" in line:
            try:
                tempo_total = float(line.split(":")[1].strip().split(" ")[0])
            except ValueError:
                pass
    
    if tempo_total == 0.0 and "Erro: Nao encontrei o mestre" in stderr_mestre:
        print("Erro ao iniciar o mestre ou workers. Verifique as mensagens de erro.")
        print("Mestre STDERR:", stderr_mestre)
        for i, p_worker in enumerate(processos_workers):
            print(f"Worker {i} STDERR:", p_worker.stderr.read())
        raise RuntimeError("Falha na execução distribuída")

    return tempo_total

if __name__ == '__main__':
    # Exemplo de uso
    tempo = executar_distribuido(100, 100, 20, 0.05, 3, 42, 2, 5000)
    print(f"Tempo de execução distribuída: {tempo:.4f}s")
