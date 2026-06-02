"""Gerador de banner ASCII — Mission Control AI."""
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
import argparse

console = Console()

def gerar_banner():
    """Gera o banner ASCII colorido da Mission Control AI."""
    linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))

def listar_fontes():
    """Lista todas as fontes disponíveis no PyFiglet."""
    fontes = pyfiglet.FigletFont.getFonts()
    for fonte in sorted(fontes):
        console.print(fonte, style="#8484A0")
    console.print(f"\nTotal: {len(fontes)} fontes disponíveis", style="bold #06B6D4")

def testar_fonte(font, text):
    """Testa uma fonte específica com um texto."""
    resultado = pyfiglet.figlet_format(text, font=font)
    console.print(Text(resultado, style="bold #06B6D4"))

def demo_fontes():
    """Demonstra 8 fontes diferentes."""
    fontes_demo = ["ansi_shadow", "slant", "big", "banner3", "block", "bubble", "digital", "doom"]
    for fonte in fontes_demo:
        console.print(f"\n── Fonte: {fonte} ──", style="italic #8484A0")
        resultado = pyfiglet.figlet_format("Mission Control", font=fonte)
        console.print(Text(resultado, style="bold #06B6D4"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII")
    parser.add_argument("-fonts", action="store_true", help="Lista todas as fontes")
    parser.add_argument("-font", type=str, help="Fonte específica para testar")
    parser.add_argument("-text", type=str, default="Mission Control AI", help="Texto para o banner")
    parser.add_argument("-demo", action="store_true", help="Demonstra 8 fontes")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demo_fontes()
    elif args.font:
        testar_fonte(args.font, args.text)
    else:
        gerar_banner()