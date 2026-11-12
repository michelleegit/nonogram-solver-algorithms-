# Nonograma — Comparação de Algoritmos de Resolução

Projeto desenvolvido em Python para resolução de puzzles Nonograma, utilizando três abordagens algorítmicas: **Backtracking, Algoritmo Genético e Método Híbrido**.

## Sobre o projeto

Nonograma é um puzzle lógico em que o objetivo é preencher células de uma grade de acordo com pistas numéricas posicionadas nas linhas e colunas.

Este projeto implementa três estratégias para resolver o problema e permite comparar seus resultados em diferentes instâncias.

## Algoritmos implementados

### 1. Backtracking

Método de busca exata que explora possibilidades de preenchimento do tabuleiro, utilizando restrições para orientar a busca e descartar configurações inválidas.

### 2. Algoritmo Genético

Método de otimização baseado em uma população de soluções candidatas, utilizando fitness e evolução por gerações para buscar uma configuração válida.

Por ser um método estocástico, não garante encontrar a solução em todas as execuções.

### 3. Método Híbrido

Combina as duas abordagens anteriores:

- **Algoritmo Genético:** realiza a busca inicial por uma solução candidata.
- **Backtracking:** executa o refinamento da solução.

O objetivo é combinar a exploração do espaço de busca com a capacidade de busca exata.

## Tecnologias utilizadas

- Python
- Algoritmos de busca
- Backtracking
- Algoritmos Genéticos
- Otimização combinatória

O projeto utiliza exclusivamente bibliotecas da biblioteca padrão do Python, sem dependências externas identificadas.

## Estrutura do projeto

```text
Nonograma/
├── instancias/
│   ├── nonogram_5x5.txt
│   ├── nonogram_10x10.txt
│   ├── nonogram_20x20.txt
│   └── ...
├── generator.py
├── main.py
├── metodos.py
├── metricas.py
├── tabuleiro.py
├── .gitignore
└── README.md
```

## Como executar

### Pré-requisitos

- Python 3 instalado.
- Git (opcional, para clonar o repositório).

### Execução

Clone o repositório:

```bash
git clone https://github.com/michelleegit/nonograma.git
```

Entre na pasta:

```bash
cd nonograma
```

Execute o programa informando uma instância:

```bash
python3 main.py instancias/nonogram_5x5.txt
```

Também é possível executar sem argumentos:

```bash
python3 main.py
```

Nesse caso, o programa solicitará o caminho do arquivo.

Após carregar o tabuleiro, selecione uma das opções:

1. Backtracking
2. Algoritmo Genético
3. Método Híbrido

## Resultados experimentais

Foram realizados testes com instâncias de diferentes dimensões.

| Instância | Algoritmo | Tempo (s) | Acurácia | Resultado |
|---|---|---:|---:|---|
| 5×5 | Backtracking | 0,0002 | 100% | Resolvido |
| 5×5 | Genético | 0,0027 | 100% | Resolvido |
| 5×5 | Híbrido | 0,0081 | 100% | Resolvido |
| 10×10 | Backtracking | 0,0032 | 100% | Resolvido |
| 10×10 | Genético | 1,4561 | 100% | Resolvido |
| 10×10 | Híbrido | 0,1327 | 100% | Resolvido |
| 20×20 | Backtracking | 2,3606 | 100% | Resolvido |
| 20×20 | Genético | 14,2668 | 55% | Melhor aproximação |
| 20×20 | Híbrido | 3,0871 | 100% | Resolvido |

*Observação: os tempos correspondem às execuções realizadas no ambiente de desenvolvimento. Os resultados do Algoritmo Genético e do Método Híbrido podem variar entre execuções devido à natureza estocástica desses métodos. Os valores apresentados não representam médias de múltiplas execuções.*

## Análise dos resultados

Os testes demonstraram diferenças de desempenho entre as estratégias.

- O Backtracking apresentou excelente desempenho nas instâncias menores e resolveu a instância 20×20 em aproximadamente 2,36 segundos.
- O Algoritmo Genético encontrou soluções nas instâncias 5×5 e 10×10, mas não atingiu uma solução exata na instância 20×20 dentro do limite de gerações estabelecido.
- O Método Híbrido resolveu todas as instâncias testadas, incluindo a 20×20, na qual o Algoritmo Genético isolado não encontrou a solução.

Os resultados indicam que a combinação das estratégias pode ser vantajosa em determinadas instâncias, embora sejam necessários experimentos adicionais para estabelecer conclusões gerais sobre desempenho.

