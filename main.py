import sys
import os

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

from tabuleiro import (
    limpar_tela, imprimeNonograma, console, MAGENTA, BOLD, RED
)
from metodos import resolver_backtracking, resolver_genetico, resolver_hibrido

def exibir_resultado(
    jogo: list,
    linha: int,
    coluna: int,
    nL: list,
    nC: list,
    maiorL: int,
    maiorC: int,
    cabecalhoL_visual: list,
    cabecalhoC: list,
    resultado_solver: any,
    algoritmo: str
) -> None:
    # 1. Limpa a tela e exibe a identidade visual
    limpar_tela()
    menu()

    # 2. Tabuleiro completamente resolvido
    imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC,
                     cabecalhoL_visual, cabecalhoC)

    console.print(Align.center(Text("PROCESSO FINALIZADO!", style="bold white")))
    console.print()

    # 3. Métricas em duas colunas: nome à esquerda, valor à direita
    metricas = Table.grid(padding=(0, 3))
    metricas.add_column(justify="left", style="grey62")
    metricas.add_column(justify="right", style="bold white")

    aviso = None
    if isinstance(resultado_solver, dict) and "metrics" in resultado_solver:
        for chave, valor in resultado_solver["metrics"].items():
            metricas.add_row(Text(str(chave)), Text(str(valor)))
    else:
        # Fallback: o solver ainda devolve só True/False
        status_txt = "Sim" if resultado_solver is True else "Não"
        metricas.add_row(Text("Algoritmo"), Text(algoritmo))
        metricas.add_row(Text("Dimensões"), Text(f"{linha}x{coluna}"))
        metricas.add_row(Text("Resolvido"), Text(status_txt))
        aviso = Text("O solver ainda não devolve as métricas completas "
                     "(Metrics.build()).", style="grey50")

    console.print(Align.center(Panel(
        metricas,
        title=f"[bold white]MÉTRICAS — {algoritmo.upper()}[/]",
        box=box.ROUNDED,
        border_style="grey62",
        padding=(0, 3),
        expand=False,
    )))
    if aviso:
        console.print(Align.center(aviso))
    console.print()

def menu():
    cabecalho = Text.from_markup(
        "[bold white]NONOGRAMA[/bold white]\n"
        "[grey62]Backtracking • Algoritmo Genético • Híbrido[/grey62]",
        justify="center",
    )
    console.print()
    console.print(Align.center(Panel(
        cabecalho,
        border_style="grey62",
        box=box.ROUNDED,
        padding=(0, 2),     # sem espaço vertical interno
        expand=False,
    )))


def comandos(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC):
    while True:
        tabela = Table(
            title="[bold white]MÉTODOS DE RESOLUÇÃO[/bold white]",
            box=box.ROUNDED,
            border_style="grey62",
            header_style="bold white",
            expand=False,
        )
        tabela.add_column("Opção", justify="center", style="bold white", width=8)
        tabela.add_column("Método", style="white", min_width=20)
        tabela.add_column("Descrição", style="grey62")

        tabela.add_row("1", "Backtracking",
                       "Busca exata recursiva com podas heurísticas")
        tabela.add_row("2", "Algoritmo Genético",
                       "Evolução populacional por busca estocástica")
        tabela.add_row("3", "Método Híbrido",
                       "Processamento AG → Refinamento por Backtracking")
        tabela.add_row("sair", "Encerrar",
                       "Encerra o programa")

        console.print(Align.center(tabela))
        console.print()

        entrada = input(BOLD("Escolha uma opção (1, 2, 3) ou digite 'sair': ")).strip().lower()
        
        if not entrada:
            continue

        if entrada == "sair":
            limpar_tela()
            print(BOLD("Obrigado por jogar ") + MAGENTA("<3") + BOLD("!"))
            break
            
        elif entrada in ["1", "2", "3"]:
            if entrada == "1":
                res = resolver_backtracking(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "BT")
            elif entrada == "2":
                res = resolver_genetico(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "AG")
            elif entrada == "3":
                res = resolver_hibrido(jogo, linha, coluna, cabecalhoL_visual, cabecalhoC)
                exibir_resultado(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC, res, "HD")
            break
        else:
            limpar_tela()
            menu()
            imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC)
            print(RED("\nOpção Inválida! Escolha 1, 2, 3 ou digite 'sair'.\n"))


def main():
    if len(sys.argv) == 1:
        arq = input("Por favor, digite o nome do arquivo do nonograma (ex: instancias/nonogram_5x5.txt):\n").strip()
        limpar_tela()
    else:
        arq = sys.argv[1]

    try:
        with open(arq, "r", encoding="utf-8") as file:
            linhas_arquivo = [l.strip() for l in file.readlines() if l.strip()]
    except FileNotFoundError:
        print(f"Erro ao abrir o arquivo {arq}")
        return

    if not linhas_arquivo:
        return

    dimensoes = linhas_arquivo[0].split()
    linha, coluna = int(dimensoes[0]), int(dimensoes[1])

    cabecalhoL, cabecalhoC = [], []
    idx = 1
    for _ in range(linha):
        cabecalhoL.append(list(map(int, linhas_arquivo[idx].split())))
        idx += 1

    for _ in range(coluna):
        cabecalhoC.append(list(map(int, linhas_arquivo[idx].split())))
        idx += 1

    nL = [len(clue) for clue in cabecalhoL]
    nC = [len(clue) for clue in cabecalhoC]
    maiorL, maiorC = max(nL), max(nC)

    cabecalhoL_visual = [clue[::-1] for clue in cabecalhoL]
    jogo = [['.' for _ in range(coluna)] for _ in range(linha)]

    # --- FLUXO DO PROGRAMA ---
    limpar_tela()
    menu()  # 1. Logo
    imprimeNonograma(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC) # 2. Matriz Lida
    comandos(jogo, linha, coluna, nL, nC, maiorL, maiorC, cabecalhoL_visual, cabecalhoC) # 3. Menu de Opções


if __name__ == "__main__":
    main()