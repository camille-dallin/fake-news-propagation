
import pandas as pd
import matplotlib.pyplot as plt
import os

def gerar_graficos():
    caminho_csv = os.path.join("experimentos", "resultados.csv")
    if not os.path.exists(caminho_csv):
        print(f"Erro: {caminho_csv} nao encontrado.")
        return

    df = pd.read_csv(caminho_csv)
    
    # Filtra apenas o maior cenário para os gráficos de Speedup e Eficiência por Threads/Workers
    # para não poluir o gráfico, ou gera múltiplos gráficos.
    maior_matriz = df['matriz'].unique()[-1]
    df_maior = df[df['matriz'] == maior_matriz]

    # 1. Gráfico de Speedup
    plt.figure(figsize=(10, 6))
    
    # Paralela
    df_par = df_maior[df_maior['versao'] == 'Paralela']
    plt.plot(df_par['threads_workers'], df_par['speedup'], marker='o', label='Paralela (Threads)')
    
    # Distribuída
    df_dist = df_maior[df_maior['versao'] == 'Distribuida']
    plt.plot(df_dist['threads_workers'], df_dist['speedup'], marker='s', label='Distribuida (Workers)')
    
    # Ideal
    plt.plot([1, 8], [1, 8], 'k--', label='Speedup Ideal')
    
    plt.title(f'Speedup - Matriz {maior_matriz}')
    plt.xlabel('Número de Threads / Workers')
    plt.ylabel('Speedup')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experimentos", "grafico_speedup.png"))
    plt.close()

    # 2. Gráfico de Eficiência
    plt.figure(figsize=(10, 6))
    
    # Paralela
    plt.plot(df_par['threads_workers'], df_par['eficiencia'], marker='o', label='Paralela (Threads)')
    
    # Distribuída
    plt.plot(df_dist['threads_workers'], df_dist['eficiencia'], marker='s', label='Distribuida (Workers)')
    
    plt.title(f'Eficiência - Matriz {maior_matriz}')
    plt.xlabel('Número de Threads / Workers')
    plt.ylabel('Eficiência')
    plt.ylim(0, 1.1)
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experimentos", "grafico_eficiencia.png"))
    plt.close()

    # 3. Comparação de Tempo por Tamanho de Matriz (com 4 threads/workers)
    plt.figure(figsize=(10, 6))
    
    n_exec = 4
    
    versoes = ['Sequencial', 'Paralela', 'Distribuida']
    matrizes = df['matriz'].unique()
    
    for versao in versoes:
        data = df[(df['versao'] == versao) & (df['threads_workers'] == (1 if versao == 'Sequencial' else n_exec))]
        # Agrupa por matriz e tira a média dos diferentes cenários de gerações/espalhadores para simplificar
        data_grouped = data.groupby('matriz')['tempo_medio'].mean().reindex(matrizes)
        plt.plot(matrizes, data_grouped, marker='o', label=f'{versao} (1 thread/worker)' if versao == 'Sequencial' else f'{versao} ({n_exec} threads/workers)')

    plt.title('Tempo de Execução por Tamanho de Matriz')
    plt.xlabel('Tamanho da Matriz')
    plt.ylabel('Tempo Médio (s)')
    plt.yscale('log') # Escala logarítmica para melhor visualização
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join("experimentos", "grafico_tempos.png"))
    plt.close()

    print("Graficos gerados com sucesso na pasta 'experimentos'!")

if __name__ == "__main__":
    gerar_graficos()
