import pulp as plp

def resolver_pl(titulo, tipo_otimizacao, coeficientes_objetivo, restricoes):
    """
    Função genérica para resolver um problema de programação linear usando PuLP.
    Argumentos:
        titulo (str): O nome do problema a ser exibido.
        tipo_otimizacao (plp.LpMaximize ou plp.LpMinimize): O objetivo (maximizar ou minimizar).
        coeficientes_objetivo (list): Lista de coeficientes da função objetivo.
        restricoes (list of dict): Uma lista de dicionários, onde cada um representa uma restrição.
    """
    print(f"\n--- {titulo} ---")

    # 1. Cria o modelo
    modelo = plp.LpProblem(titulo, tipo_otimizacao)

    # 2. Cria as variáveis de decisão (assumindo 2 variáveis: x1 e x2)
    x1 = plp.LpVariable('x1', lowBound=0, cat=plp.LpContinuous)
    x2 = plp.LpVariable('x2', lowBound=0, cat=plp.LpContinuous)
    variaveis = [x1, x2]

    # 3. Adiciona a função objetivo
    modelo += plp.lpSum([coeficientes_objetivo[i] * variaveis[i] for i in range(len(variaveis))]), "Funcao_Objetivo"

    # 4. Adiciona as restrições
    for i, r in enumerate(restricoes):
        expressao = plp.lpSum([r['coefs'][j] * variaveis[j] for j in range(len(variaveis))])

        if r['op'] == '<=':
            modelo += expressao <= r['rhs'], f"Restricao_{i + 1}"
        elif r['op'] == '>=':
            modelo += expressao >= r['rhs'], f"Restricao_{i + 1}"
        elif r['op'] == '==':
            modelo += expressao == r['rhs'], f"Restricao_{i + 1}"

    # 5. Resolve o modelo
    modelo.solve()

    # 6. Exibe os resultados
    print(f"Status: {plp.LpStatus[modelo.status]}")
    if modelo.status == plp.LpStatusOptimal:
        print("Solução Ótima:")
        for var in modelo.variables():
            print(f"  {var.name} = {var.varValue}")
        print(f"Valor Ótimo (Z): {plp.value(modelo.objective)}\n")
    else:
        print("Não foi encontrada uma solução ótima (o problema pode ser inviável ou ilimitado).\n")


# Bloco principal
if __name__ == "__main__":

    # --- Definição dos Dados dos 5 Problemas ---

    lista_de_problemas = [
        {
            "titulo": "Problema 1: Maximizar 4*x1 + 3*x2",
            "tipo": plp.LpMaximize,
            "objetivo": [4, 3],
            "restricoes": [
                {'coefs': [1, 3], 'op': '<=', 'rhs': 7},
                {'coefs': [2, 2], 'op': '<=', 'rhs': 8},
                {'coefs': [1, 1], 'op': '<=', 'rhs': 3},
                {'coefs': [0, 1], 'op': '<=', 'rhs': 2}
            ]
        },
        {
            "titulo": "Problema 2: Minimizar 8*x1 + 10*x2",
            "tipo": plp.LpMinimize,
            "objetivo": [8, 10],
            "restricoes": [
                {'coefs': [-1, 1], 'op': '<=', 'rhs': 2},
                {'coefs': [4, 5], 'op': '>=', 'rhs': 20},
                {'coefs': [1, 0], 'op': '<=', 'rhs': 6},
                {'coefs': [0, 1], 'op': '>=', 'rhs': 4}
            ]
        },
        {
            "titulo": "Problema 3: Minimizar x1 + 2*x2",
            "tipo": plp.LpMinimize,
            "objetivo": [1, 2],
            "restricoes": [
                {'coefs': [1, 1], 'op': '>=', 'rhs': 1},
                {'coefs': [-5, 2], 'op': '>=', 'rhs': -10},
                {'coefs': [3, 5], 'op': '>=', 'rhs': 15}
            ]
        },
        {
            "titulo": "Problema 4: Maximizar 4*x1 + 8*x2",
            "tipo": plp.LpMaximize,
            "objetivo": [4, 8],
            "restricoes": [
                {'coefs': [3, 2], 'op': '<=', 'rhs': 18},
                {'coefs': [1, 1], 'op': '<=', 'rhs': 5},
                {'coefs': [1, 0], 'op': '<=', 'rhs': 4}
            ]
        },
        {
            "titulo": "Problema 5: Maximizar x1 + 3*x2",
            "tipo": plp.LpMaximize,
            "objetivo": [1, 3],
            "restricoes": [
                {'coefs': [4, 1], 'op': '>=', 'rhs': 30},
                {'coefs': [10, 2], 'op': '<=', 'rhs': 10}
            ]
        }
    ]

    # --- Execução dos 5 Problemas ---

    for problema in lista_de_problemas:
        resolver_pl(
            titulo=problema["titulo"],
            tipo_otimizacao=problema["tipo"],
            coeficientes_objetivo=problema["objetivo"],
            restricoes=problema["restricoes"]
        )