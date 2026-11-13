import os
import sys

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# Paleta (grey0 = preto ... grey100 = branco)
COR_DICA     = "grey85"      # números das dicas
COR_VAZIO    = "grey46"      # pontinho da célula vazia
COR_CHEIO    = "on #2f5fd0"  # bloco preenchido (azul; "on" = cor de fundo)
COR_BORDA    = "grey62"      # moldura
COR_TITULO   = "bold white"
COR_DESTAQUE = "cyan"        # dimensões no título

# Cores e formato de texto padrão ANSI
ANSI_RESET = "\x1b[0m"
ANSI_BOLD = "\x1b[1m"
ANSI_BG_COLOR_BLACK = "\x1b[40m"
ANSI_BG_COLOR_CYAN = "\x1b[46m"
ANSI_BG_COLOR_GREEN = "\x1b[42m"
ANSI_BG_COLOR_MAGENTA = "\x1b[45m"

def BG_BLACK(string): return f"{ANSI_BG_COLOR_BLACK}{string}{ANSI_RESET}"
def BG_CYAN(string): return f"{ANSI_BG_COLOR_CYAN}{string}{ANSI_RESET}"
def BG_GREEN(string): return f"{ANSI_BG_COLOR_GREEN}{string}{ANSI_RESET}"
def BG_MAGENTA(string): return f"{ANSI_BG_COLOR_MAGENTA}{string}{ANSI_RESET}"
def BOLD(string): return f"{ANSI_BOLD}{string}{ANSI_RESET}"
def RED(string): return f"\x1b[31m{string}\x1b[0m"
def YELLOW(string): return f"\x1b[33m{string}\x1b[0m"
def BLUE(string): return f"\x1b[34m{string}\x1b[0m"
def MAGENTA(string): return f"\x1b[35m{string}\x1b[0m"

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def indice_para_letras(n: int) -> str:
    """Converte um índice numérico (0, 1, 2...) em letras estilo Excel (A, B... Z, AA, AB...)"""
    resultado = ""
    n += 1
    while n > 0:
        n, resto = divmod(n - 1, 26)
        resultado = chr(65 + resto) + resultado
    return resultado

def letras_para_indice(letras: str) -> int:
    """Converte letras (A, AA, etc.) de volta para um índice numérico (0, 1, 2...)"""
    num = 0
    for letra in letras.upper():
        if 'A' <= letra <= 'Z':
            num = num * 26 + (ord(letra) - ord('A') + 1)
        else:
            raise ValueError
    return num - 1

def imprimeNonograma(jogo, l, c, nL, nC, maiorL, maiorC, cabecalhoL, cabecalhoC):
    # Largura da célula: 2 deixa quadrada; 3 se alguma dica tiver 2 dígitos
    maior_dica = max(max(d) for d in cabecalhoL + cabecalhoC)
    larg = max(2, len(str(maior_dica)) + 1)

    grade = Table.grid(padding=0)       # tabela sem bordas
    grade.add_column(justify="right")   # dicas das linhas
    grade.add_column(width=2)           # espaço entre dicas e tabuleiro
    for _ in range(c):
        grade.add_column(justify="center", width=larg)

    # Dicas das colunas (alinhadas pela base)
    for i in range(maiorC):
        linha = [Text(""), Text("")]
        for j in range(c):
            pos = i - (maiorC - nC[j])
            linha.append(
                Text(str(cabecalhoC[j][pos]), style=COR_DICA) if pos >= 0 else Text("")
            )
        grade.add_row(*linha)

    # Linhas do tabuleiro
    for i in range(l):
        # reversed: o main entrega as dicas de linha invertidas
        dicas = Text(" ".join(str(x) for x in reversed(cabecalhoL[i])), style=COR_DICA)
        linha = [dicas, Text("")]
        for j in range(c):
            if jogo[i][j].lower() == "x":
                linha.append(Text(" " * larg, style=COR_CHEIO))   # preenchida
            else:
                linha.append(Text("·", style=COR_VAZIO))          # vazia
        grade.add_row(*linha)

    console.print(Align.center(Panel(
        grade,
        title=f"[{COR_TITULO}]NONOGRAMA[/] [{COR_DESTAQUE}]{l} × {c}[/]",
        box=box.ROUNDED,
        border_style=COR_BORDA,
        padding=(0, 3),
        expand=False,
    )))

def mudaNonograma(jogo, r_str, c_str, l, c, oper):
    try:
        li = letras_para_indice(r_str)
        co = letras_para_indice(c_str)
    except ValueError:
        print(RED("\nCoordenadas inválidas! Use letras do alfabeto (Ex: A, Z, AA)."))
        return

    if co >= c or li >= l or li < 0 or co < 0:
        print(f"Posição incorreta! Extrapola os limites de {indice_para_letras(l-1)} x {indice_para_letras(c-1)}")
    else:
        jogo[li][co] = oper

def verifica(jogo, l, c, nL, nC, cL, cC):
    contL = [0] * l
    contC = [0] * c
    for i in range(l):
        for j in range(c):
            if jogo[i][j] == 'x':
                contL[i] += 1
                contC[j] += 1

    somL = [sum(cL[i]) for i in range(l)]
    somC = [sum(cC[i]) for i in range(c)]

    linhas_completas = sum(1 for i in range(l) if somL[i] == contL[i])
    colunas_completas = sum(1 for i in range(c) if somC[i] == contC[i])

    if (linhas_completas == l) and (colunas_completas == c):
        return 1
    return 0