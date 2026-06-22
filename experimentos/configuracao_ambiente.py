"""Coleta e registra a configuracao do ambiente de execucao dos experimentos.

Atende ao item 'Configuracao Experimental' do enunciado: processador, nucleos,
memoria RAM, sistema operacional, linguagem e versao do interpretador.
"""
import os
import platform
import subprocess
import sys


def _powershell(comando):
    try:
        saida = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", comando],
            stderr=subprocess.DEVNULL, text=True, timeout=15)
        return saida.strip()
    except Exception:
        return None


def coletar_configuracao():
    info = {}

    # CPU + nucleos (Windows via PowerShell; fallback multiplataforma)
    nome_cpu = _powershell("(Get-CimInstance Win32_Processor).Name")
    nucleos_fisicos = _powershell("(Get-CimInstance Win32_Processor).NumberOfCores")
    nucleos_logicos = _powershell("(Get-CimInstance Win32_Processor).NumberOfLogicalProcessors")
    ram_bytes = _powershell("(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory")

    info["processador"] = (nome_cpu or platform.processor() or "desconhecido").strip()
    info["nucleos_fisicos"] = nucleos_fisicos or "n/d"
    info["nucleos_logicos"] = nucleos_logicos or str(os.cpu_count())
    if ram_bytes and ram_bytes.isdigit():
        info["memoria_ram_gb"] = f"{int(ram_bytes) / (1024 ** 3):.1f} GB"
    else:
        info["memoria_ram_gb"] = "n/d"

    info["sistema_operacional"] = f"{platform.system()} {platform.release()} ({platform.version()})"
    info["linguagem"] = f"{platform.python_implementation()} (Python)"
    info["versao_interpretador"] = platform.python_version()
    info["arquitetura"] = platform.machine()
    info["ambiente_execucao"] = "Execucao local; versao distribuida via Sockets TCP em localhost"

    return info


def formatar(info):
    rotulos = {
        "processador": "Processador",
        "nucleos_fisicos": "Nucleos fisicos",
        "nucleos_logicos": "Nucleos logicos",
        "memoria_ram_gb": "Memoria RAM",
        "sistema_operacional": "Sistema operacional",
        "linguagem": "Linguagem",
        "versao_interpretador": "Versao do interpretador",
        "arquitetura": "Arquitetura",
        "ambiente_execucao": "Ambiente de execucao",
    }
    linhas = ["=== CONFIGURACAO EXPERIMENTAL ===", ""]
    for chave, rotulo in rotulos.items():
        linhas.append(f"{rotulo:<26}: {info[chave]}")
    return "\n".join(linhas)


def main():
    info = coletar_configuracao()
    texto = formatar(info)
    print(texto)

    caminho = os.path.join("experimentos", "configuracao.txt")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto + "\n")
    print(f"\nConfiguracao salva em {caminho}")


if __name__ == "__main__":
    main()
