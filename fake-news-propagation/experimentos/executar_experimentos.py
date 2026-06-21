
import time
import csv
import os
import sys
from sequencial.simulacao_sequencial import executarsimulacaosequencial
from paralelo.simulacao_paralela import SimulacaoParalela
from experimentos.executar_distribuido import executar_distribuido

def executar_bateria_testes():
    cenarios = [
        {"linhas": 100, "colunas": 100, "geracoes": 10, "percentual_espalhadores": 0.01},
        {"linhas": 100, "colunas": 100, "geracoes": 50, "percentual_espalhadores": 0.05},
        {"linhas": 100, "colunas": 100, "geracoes": 100, "percentual_espalhadores": 0.10},
        {"linhas": 200, "colunas": 200, "geracoes": 10, "percentual_espalhadores": 0.01},
        {"linhas": 200, "colunas": 200, "geracoes": 50, "percentual_espalhadores": 0.05},
        {"linhas": 200, "colunas": 200, "geracoes": 100, "percentual_espalhadores": 0.10},
        {"linhas": 500, "colunas": 500, "geracoes": 10, "percentual_espalhadores": 0.01},
        {"linhas": 500, "colunas": 500, "geracoes": 50, "percentual_espalhadores": 0.05},
        {"linhas": 500, "colunas": 500, "geracoes": 100, "percentual_espalhadores": 0.10}
    ]
    
    threads_teste = [2, 4, 8]
    workers_teste = [1, 2, 4] # Adicionado para testes distribuídos
    repeticoes = 3 # Roda 3 vezes cada cenário para tirar a média justa
    
    resultados = []
    
    print("=== INICIANDO BATERIA DE EXPERIMENTOS ===")
    
    for cenario in cenarios:
        l = cenario["linhas"]
        c = cenario["colunas"]
        g = cenario["geracoes"]
        p = cenario["percentual_espalhadores"]
        limiar = 3 # Fixo para este experimento
        semente = 42 # Fixo para este experimento
        porta_distribuida = 5000 # Porta para o mestre
        
        print(f"\nTestando Matriz {l}x{c}, {g} geracoes, {p*100:.0f}% espalhadores...")
        
        # 1. Teste Sequencial (Nossa base de tempo)
        tempo_seq_total = 0
        for _ in range(repeticoes):
            res = executarsimulacaosequencial(l, c, g, p, limiar, semente, False)
            tempo_seq_total += res["tempototal"]
        tempo_seq_medio = tempo_seq_total / repeticoes
        
        resultados.append({
            "matriz": f"{l}x{c}",
            "geracoes": g,
            "percentual_espalhadores": p,
            "versao": "Sequencial",
            "threads_workers": 1,
            "tempo_medio": tempo_seq_medio,
            "speedup": 1.0,
            "eficiencia": 1.0
        })
        print(f"  -> Sequencial: {tempo_seq_medio:.4f}s")
        
        # 2. Teste Paralelo
        for t in threads_teste:
            tempo_par_total = 0
            for _ in range(repeticoes):
                sim = SimulacaoParalela(l, c, g, p, limiar, semente, t)
                tempo = sim.executar()
                tempo_par_total += tempo
            tempo_par_medio = tempo_par_total / repeticoes
            
            # Cálculos exigidos pelo professor
            speedup = tempo_seq_medio / tempo_par_medio
            eficiencia = speedup / t
            
            resultados.append({
                "matriz": f"{l}x{c}",
                "geracoes": g,
                "percentual_espalhadores": p,
                "versao": "Paralela",
                "threads_workers": t,
                "tempo_medio": tempo_par_medio,
                "speedup": speedup,
                "eficiencia": eficiencia
            })
            print(f"  -> Paralela ({t} threads): {tempo_par_medio:.4f}s | Speedup: {speedup:.2f}x | Efi: {eficiencia:.2f}")

        # 3. Teste Distribuído
        for w in workers_teste:
            tempo_dist_total = 0
            for _ in range(repeticoes):
                tempo = executar_distribuido(l, c, g, p, limiar, semente, w, porta_distribuida)
                tempo_dist_total += tempo
            tempo_dist_medio = tempo_dist_total / repeticoes

            # Cálculos exigidos pelo professor para distribuído
            speedup_dist = tempo_seq_medio / tempo_dist_medio
            eficiencia_dist = speedup_dist / w

            resultados.append({
                "matriz": f"{l}x{c}",
                "geracoes": g,
                "percentual_espalhadores": p,
                "versao": "Distribuida",
                "threads_workers": w,
                "tempo_medio": tempo_dist_medio,
                "speedup": speedup_dist,
                "eficiencia": eficiencia_dist
            })
            print(f"  -> Distribuida ({w} workers): {tempo_dist_medio:.4f}s | Speedup: {speedup_dist:.2f}x | Efi: {eficiencia_dist:.2f}")

    # Salva tudo em um arquivo CSV
    caminho_csv = os.path.join("experimentos", "resultados.csv")
    with open(caminho_csv, mode='w', newline='') as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["matriz", "geracoes", "percentual_espalhadores", "versao", "threads_workers", "tempo_medio", "speedup", "eficiencia"])
        writer.writeheader()
        writer.writerows(resultados)
        
    print(f"\nExperimentos concluidos! Resultados salvos em {caminho_csv}")

if __name__ == "__main__":
    executar_bateria_testes()
