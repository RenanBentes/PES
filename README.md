# Pesquisa Operacional

Este diretório contém scripts Python para resolução de problemas de Pesquisa Operacional. Os scripts utilizam diferentes abordagens e bibliotecas para modelar e resolver problemas de otimização de fluxo máximo.

## Descrição dos Arquivos

- `FluxodeRede.py`: Resolve o problema de fluxo em uma rede utilizando a técnica do arco imaginário e o solver do Google OR-Tools.
- `CaminhoMinimo.py`: resolve o problema do caminho mínimo com o solver do Google OR-Tools.
- `PesquisaLinear.py`: Implementa métodos de pesquisa linear para problemas de fluxo em redes.
- `PuLPLinear.py`: Utiliza a biblioteca PuLP para modelar e resolver problemas de fluxo máximo via Programação Linear.
- `SolverLinear.py`: Implementa o método Simplex para resolver problemas de Programação Linear.

## Requisitos

- Python 3.x
- OR-Tools
- PuLP
- Numpy
- Sympy

## Como Executar

Execute qualquer um dos scripts diretamente pelo terminal ou pelo PyCharm:

```
python FluxodeRede.py
```

Edite os scripts conforme necessário para testar diferentes instâncias ou métodos de resolução.

## Observações

- Cada script pode conter exemplos de uso e impressão dos resultados no console.
- Consulte os comentários nos arquivos para detalhes sobre a modelagem e as restrições implementadas.

---
