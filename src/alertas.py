"""Thresholds e regras de decisão — MobilitySat (GNSS)."""

# Thresholds conforme decisões do projeto
THRESHOLD_POTENCIA_CRITICA = 20.0
THRESHOLD_SINAL_CRITICO = 60.0
THRESHOLD_SINAL_ATENCAO = 80.0
THRESHOLD_DRIFT_CRITICO = 50.0
THRESHOLD_DRIFT_ATENCAO = 30.0
THRESHOLD_SYNC_CRITICO = 4
THRESHOLD_SYNC_ATENCAO = 6


def avaliar(dados):
    """
    Avalia os dados de telemetria e retorna lista de alertas.
    A lógica de decisão está em código Python, não no prompt da IA.
    Retorna dict com alertas e resposta_automatica.
    """
    alertas = []
    resposta_automatica = None

    # Regra 1 — Margem de potência crítica (resposta automática)
    if dados["margem_potencia"] < THRESHOLD_POTENCIA_CRITICA:
        alertas.append({
            "parametro": "Margem de potência",
            "valor": dados["margem_potencia"],
            "nivel": "RESPOSTA_AUTOMATICA",
            "mensagem": f"Potência em {dados['margem_potencia']}% — abaixo de {THRESHOLD_POTENCIA_CRITICA}%"
        })
        resposta_automatica = "⚡ MODO ECONOMIA ATIVADO: potência crítica detectada. Reduzindo operações não essenciais do satélite."

    # Regra 2 — Integridade do sinal crítica
    if dados["integridade_sinal"] < THRESHOLD_SINAL_CRITICO:
        alertas.append({
            "parametro": "Integridade do sinal L1/L5",
            "valor": dados["integridade_sinal"],
            "nivel": "CRITICO",
            "mensagem": f"Sinal em {dados['integridade_sinal']}% — operações de drones SUSPENSAS"
        })

    # Regra 3 — Integridade do sinal em atenção
    elif dados["integridade_sinal"] < THRESHOLD_SINAL_ATENCAO:
        alertas.append({
            "parametro": "Integridade do sinal L1/L5",
            "valor": dados["integridade_sinal"],
            "nivel": "ATENCAO",
            "mensagem": f"Sinal em {dados['integridade_sinal']}% — precisão degradada, alertar gestor"
        })

    # Regra 4 — Drift do oscilador crítico
    if dados["drift_oscilador"] > THRESHOLD_DRIFT_CRITICO:
        alertas.append({
            "parametro": "Drift do oscilador atômico",
            "valor": dados["drift_oscilador"],
            "nivel": "CRITICO",
            "mensagem": f"Drift em {dados['drift_oscilador']}ns — risco de posicionamento incorreto"
        })

    # Regra 5 — Drift do oscilador em atenção
    elif dados["drift_oscilador"] > THRESHOLD_DRIFT_ATENCAO:
        alertas.append({
            "parametro": "Drift do oscilador atômico",
            "valor": dados["drift_oscilador"],
            "nivel": "ATENCAO",
            "mensagem": f"Drift em {dados['drift_oscilador']}ns — desvio crescente, monitorar"
        })

    # Regra 6 — Sincronização crítica
    if dados["satellites_sync"] < THRESHOLD_SYNC_CRITICO:
        alertas.append({
            "parametro": "Sincronização com a constelação",
            "valor": dados["satellites_sync"],
            "nivel": "CRITICO",
            "mensagem": f"{dados['satellites_sync']} satélites — perda de posicionamento confiável"
        })

    # Regra 7 — Sincronização em atenção
    elif dados["satellites_sync"] < THRESHOLD_SYNC_ATENCAO:
        alertas.append({
            "parametro": "Sincronização com a constelação",
            "valor": dados["satellites_sync"],
            "nivel": "ATENCAO",
            "mensagem": f"{dados['satellites_sync']} satélites — precisão reduzida, operar com cautela"
        })

    return {
        "alertas": alertas,
        "resposta_automatica": resposta_automatica,
        "tem_critico": any(a["nivel"] == "CRITICO" for a in alertas),
        "tem_atencao": any(a["nivel"] == "ATENCAO" for a in alertas),
        "status_geral": _calcular_status(alertas)
    }

def _calcular_status(alertas):
    """Calcula o status geral da missão baseado nos alertas."""
    if any(a["nivel"] == "RESPOSTA_AUTOMATICA" for a in alertas):
        return "EMERGÊNCIA"
    if any(a["nivel"] == "CRITICO" for a in alertas):
        return "CRÍTICO"
    if any(a["nivel"] == "ATENCAO" for a in alertas):
        return "ATENÇÃO"
    return "NORMAL"


def formatar_alertas(resultado):
    """
    Formata os alertas para exibição legível no terminal.
    """
    if not resultado["alertas"]:
        return "✅ Todos os parâmetros dentro dos limites normais."

    linhas = []

    if resultado["resposta_automatica"]:
        linhas.append(resultado["resposta_automatica"])

    for alerta in resultado["alertas"]:
        if alerta["nivel"] == "CRITICO":
            linhas.append(f"🔴 CRÍTICO — {alerta['mensagem']}")
        elif alerta["nivel"] == "ATENCAO":
            linhas.append(f"🟡 ATENÇÃO — {alerta['mensagem']}")
        elif alerta["nivel"] == "RESPOSTA_AUTOMATICA":
            linhas.append(f"⚡ AUTO — {alerta['mensagem']}")

    return "\n".join(linhas)