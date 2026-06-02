"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))

def show_banner():
    """Exibe banner ASCII colorido no início."""
    banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    console.print(Text(banner, style="bold #06B6D4"))
    console.print(Panel.fit(
        "Sistema de monitoramento de satélite GNSS — MobilitySat\n"
        "Trilha: MobilitySat · Persona: Gestor de frota logística\n"
        "Use /help para ver os comandos · /exit para sair.\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="◆ MISSION CONTROL AI",
        border_style="#06B6D4"
    ))

def show_response(text):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(text, title="◆ Mission Control",
                        subtitle=now, border_style="#06B6D4"))

def show_help():
    """Exibe tabela de comandos disponíveis."""
    table = Table(title="Comandos disponíveis", border_style="#06B6D4")
    table.add_column("Comando", style="#06B6D4")
    table.add_column("Descrição", style="white")
    table.add_row("/help", "Exibe esta tabela de comandos")
    table.add_row("/status", "Exibe snapshot atual da telemetria")
    table.add_row("/about", "Informações sobre o sistema")
    table.add_row("/clear", "Limpa o terminal")
    table.add_row("/exit", "Encerra o sistema")
    console.print(table)

def show_about():
    """Exibe informações sobre o sistema."""
    console.print(Panel.fit(
        "Mission Control AI — MobilitySat\n"
        "Sistema de monitoramento de satélite GNSS com IA generativa.\n\n"
        "Parâmetros monitorados:\n"
        "  · Margem de potência (%)\n"
        "  · Integridade do sinal L1/L5 (%)\n"
        "  · Drift do oscilador atômico (ns)\n"
        "  · Sincronização com a constelação (satélites)\n\n"
        "Setor de impacto: Mobilidade e logística\n"
        "Persona: Gestor de frota logística\n"
        "FIAP · Global Solution 2026.1",
        title="◆ Sobre o sistema",
        border_style="#A855F7"
    ))

def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "\n⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="yellow"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("Encerrando Mission Control AI...", style="#06B6D4")
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue

        if user_input == "/about":
            show_about()
            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        # Qualquer outra entrada vai para o motor de análise
        resposta = engine.analyze(user_input)
        show_response(resposta)