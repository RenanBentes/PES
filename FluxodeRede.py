from ortools.linear_solver import pywraplp


def resolver_fluxo_com_pl_arco_imaginario():
    """
    Resolve o problema de fluxo máximo utilizando a técnica do arco imaginário
    e o solver de Programação Linear do Google OR-Tools.
    """
    # 1. Instanciar o Solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # Mapeamento dos nós: A=0, 1=1, 2=2, 3=3, 4=4, B=5

    # 2. Definir as Variáveis de Decisão (Fluxo em cada arco)
    # Inclui um arco imaginário de B (5) para A (0) sem limite de capacidade.
    f = {
        (0, 1): solver.NumVar(0, 40, 'f_A1'),
        (0, 2): solver.NumVar(0, 30, 'f_A2'),
        (1, 3): solver.NumVar(0, 30, 'f_13'),
        (1, 4): solver.NumVar(0, 20, 'f_14'),
        (2, 4): solver.NumVar(0, 30, 'f_24'),
        (3, 5): solver.NumVar(0, 20, 'f_3B'),
        (4, 5): solver.NumVar(0, 40, 'f_4B'),
        (5, 0): solver.NumVar(0, solver.infinity(), 'f_BA_imaginario'),  # Arco imaginário
    }

    # 3. Definir as Restrições de Conservação de Fluxo para TODOS os nós
    # Com o arco de retorno, todo nó deve ter fluxo de entrada = fluxo de saída.

    # Nó A (0): Fluxo que entra (imaginário) = Fluxo que sai
    solver.Add(f[5, 0] == f[0, 1] + f[0, 2], 'Conservacao_no_A')

    # Nó 1:
    solver.Add(f[0, 1] == f[1, 3] + f[1, 4], 'Conservacao_no_1')

    # Nó 2:
    solver.Add(f[0, 2] == f[2, 4], 'Conservacao_no_2')

    # Nó 3:
    solver.Add(f[1, 3] == f[3, 5], 'Conservacao_no_3')

    # Nó 4:
    solver.Add(f[1, 4] + f[2, 4] == f[4, 5], 'Conservacao_no_4')

    # Nó B (5): Fluxo que entra = Fluxo que sai (imaginário)
    solver.Add(f[3, 5] + f[4, 5] == f[5, 0], 'Conservacao_no_B')

    # 4. Definir a Função-Objetivo
    # Maximizar o fluxo no arco imaginário, que representa o fluxo total.
    solver.Maximize(f[5, 0])

    # 5. Chamar o Solver
    status = solver.Solve()

    # 6. Exibir os Resultados
    if status == pywraplp.Solver.OPTIMAL:
        print('--- Solução Ótima Encontrada (com Arco Imaginário) ---')
        print(f'Fluxo Máximo Total: {solver.Objective().Value():.2f} m³/s')
        print('\nFluxo em cada gasoduto:')

        nomes_nos = {0: 'A', 1: '1', 2: '2', 3: '3', 4: '4', 5: 'B'}

        for (i, j), var in f.items():
            # Não exibir o arco imaginário no resultado final dos fluxos
            if (i, j) == (5, 0):
                continue
            if var.solution_value() > 1e-6:
                no_inicio = nomes_nos[i]
                no_fim = nomes_nos[j]
                print(f'  - Fluxo do Nó {no_inicio} para {no_fim}: {var.solution_value():.2f} m³/s')
    else:
        print('Não foi possível encontrar uma solução ótima.')


# Executar a função
resolver_fluxo_com_pl_arco_imaginario()
