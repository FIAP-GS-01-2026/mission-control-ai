"""Motor de análise da Mission Control AI."""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src.telemetria import coletar, formatar
from src.alertas import avaliar, formatar_alertas

load_dotenv()

# Identificação da trilha conforme PDF seção 6.4
TRILHA = "mobilitysat"

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b", messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"

def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

class MissionEngine:
    """Motor de análise da Mission Control AI — MobilitySat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.historico = []  # memória de contexto — diferencial

    def is_ready(self):
        return True

    def status_snapshot(self):
        """Retorna texto resumindo o estado atual da telemetria."""
        dados = coletar()
        resultado = avaliar(dados)
        telemetria_fmt = formatar(dados)
        alertas_fmt = formatar_alertas(resultado)
        return f"{telemetria_fmt}\n\n{alertas_fmt}"

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""

        # Passo 1 — coletar telemetria
        dados = coletar()

        # Passo 2 — avaliar alertas em Python
        resultado = avaliar(dados)

        # Passo 3 — adicionar ciclo ao histórico (memória de contexto)
        ciclo = {
            "timestamp": dados["timestamp"],
            "status": resultado["status_geral"],
            "margem_potencia": dados["margem_potencia"],
            "integridade_sinal": dados["integridade_sinal"],
            "drift_oscilador": dados["drift_oscilador"],
            "satellites_sync": dados["satellites_sync"]
        }
        self.historico.append(ciclo)
        if len(self.historico) > 3:
            self.historico.pop(0)

        # Passo 4 — montar histórico formatado
        historico_fmt = ""
        if len(self.historico) > 1:
            historico_fmt = "\n## Histórico dos últimos ciclos\n"
            for c in self.historico[:-1]:
                historico_fmt += (
                    f"- {c['timestamp']}: status={c['status']}, "
                    f"potência={c['margem_potencia']}%, "
                    f"sinal={c['integridade_sinal']}%, "
                    f"drift={c['drift_oscilador']}ns, "
                    f"satélites={c['satellites_sync']}/12\n"
                )

        # Passo 5 — montar prompt com dados + alertas + histórico + pergunta
        prompt = f"""## Dados de telemetria atuais
- Timestamp: {dados['timestamp']}
- Margem de potência: {dados['margem_potencia']}%
- Integridade do sinal L1/L5: {dados['integridade_sinal']}%
- Drift do oscilador atômico: {dados['drift_oscilador']} ns
- Satélites sincronizados: {dados['satellites_sync']}/12

## Alertas detectados pelo sistema
Status geral: {resultado['status_geral']}
{formatar_alertas(resultado)}

{historico_fmt}
## Resposta automática do sistema
{resultado['resposta_automatica'] if resultado['resposta_automatica'] else 'Nenhuma resposta automática ativada.'}

## Pergunta do operador
{pergunta_usuario}
"""

        # Passo 6 — chamar IA
        return llm(prompt, system=self.system_prompt)