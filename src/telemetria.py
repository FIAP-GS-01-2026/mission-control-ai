"""Geração de dados simulados de telemetria — MobilitySat (GNSS)."""
import random
from datetime import datetime


def coletar():
    """
    Simula a coleta de telemetria de um satélite GNSS.
    Retorna um dicionário com os 4 parâmetros monitorados.
    """
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "margem_potencia": round(random.uniform(0, 100), 1),
        "integridade_sinal": round(random.uniform(0, 100), 1),
        "drift_oscilador": round(random.uniform(0, 100), 2),
        "satellites_sync": random.randint(0, 12)
    }


def simular_cenario(cenario="normal"):
    """
    Simula cenários específicos para testes.
    cenario: "normal" | "potencia_critica" | "sinal_critico" | "drift_critico" | "constelacao_critica"
    """
    base = coletar()

    if cenario == "potencia_critica":
        base["margem_potencia"] = round(random.uniform(0, 19), 1)

    elif cenario == "sinal_critico":
        base["integridade_sinal"] = round(random.uniform(0, 59), 1)

    elif cenario == "sinal_atencao":
        base["integridade_sinal"] = round(random.uniform(60, 79), 1)

    elif cenario == "drift_critico":
        base["drift_oscilador"] = round(random.uniform(51, 100), 2)

    elif cenario == "drift_atencao":
        base["drift_oscilador"] = round(random.uniform(31, 50), 2)

    elif cenario == "constelacao_critica":
        base["satellites_sync"] = random.randint(0, 3)

    elif cenario == "constelacao_atencao":
        base["satellites_sync"] = random.randint(4, 5)

    return base


def formatar(dados):
    """
    Formata os dados de telemetria para exibição legível no terminal.
    """
    return (
        f"📡 Telemetria GNSS — {dados['timestamp']}\n"
        f"  ⚡ Margem de potência:          {dados['margem_potencia']}%\n"
        f"  📶 Integridade do sinal L1/L5:  {dados['integridade_sinal']}%\n"
        f"  ⏱  Drift do oscilador atômico:  {dados['drift_oscilador']} ns\n"
        f"  🛰  Satélites sincronizados:     {dados['satellites_sync']}/12"
    )