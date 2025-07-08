from ortools.linear_solver import pywraplp

def resolver_caminho_minimo_pl():
    """
    Formula e resolve o problema do caminho mínimo como um problema de
    Programação Linear usando o solver do Google OR-Tools.
    """
    # 1. Instanciar o Solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        return

    # 2. Mapear os nós (cidades) para índices numéricos
    node_map = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
        'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10
    }
    nodes = list(node_map.keys())
    num_nodes = len(nodes)
    
    # Mapeamento inverso para exibir o resultado
    reverse_node_map = {v: k for k, v in node_map.items()}

    # 3. Definir os Dados do Problema (Arcos e Custos)
    arcos_com_custos = [
        ('A', 'B', 8), ('A', 'C', 5), ('A', 'D', 7),
        ('B', 'E', 6), ('B', 'F', 2),
        ('C', 'B', 5), ('C', 'F', 4),
        ('D', 'F', 4), ('D', 'G', 2),
        ('E', 'H', 4),
        ('F', 'E', 4), ('F', 'H', 2), ('F', 'I', 5), ('F', 'G', 4),
        ('G', 'I', 2), ('G', 'J', 4),
        ('H', 'K', 4),
        ('I', 'H', 4), ('I', 'K', 5),
        ('J', 'I', 2), ('J', 'K', 4),
    ]

    # 4. Definir as Variáveis de Decisão
    # x[i, j] é uma variável binária que é 1 se o arco (i, j) está no caminho, e 0 caso contrário.
    x = {}
    for inicio, fim, custo in arcos_com_custos:
        i = node_map[inicio]
        j = node_map[fim]
        x[i, j] = solver.BoolVar(f'x_{inicio}{fim}')

    # 5. Definir as Restrições de Conservação de Fluxo
    start_node_idx = node_map['A']
    end_node_idx = node_map['K']

    for k_idx in range(num_nodes):
        # Fluxo que entra no nó k
        fluxo_entrada = solver.Sum([x[i, k_idx] for i, j in x if j == k_idx])
        # Fluxo que sai do nó k
        fluxo_saida = solver.Sum([x[k_idx, j] for i, j in x if i == k_idx])

        if k_idx == start_node_idx:
            # Nó inicial (A): fluxo líquido de saída deve ser 1
            solver.Add(fluxo_saida - fluxo_entrada == 1, f'Conservacao_{nodes[k_idx]}')
        elif k_idx == end_node_idx:
            # Nó final (K): fluxo líquido de entrada deve ser 1
            solver.Add(fluxo_saida - fluxo_entrada == -1, f'Conservacao_{nodes[k_idx]}')
        else:
            # Nós intermediários: fluxo que entra = fluxo que sai
            solver.Add(fluxo_saida - fluxo_entrada == 0, f'Conservacao_{nodes[k_idx]}')

    # 6. Definir a Função-Objetivo
    # Minimizar o custo total do caminho.
    custo_total = solver.Sum(custo * x[node_map[inicio], node_map[fim]] for inicio, fim, custo in arcos_com_custos)
    solver.Minimize(custo_total)

    # 7. Chamar o Solver
    status = solver.Solve()

    # 8. Exibir os Resultados
    if status == pywraplp.Solver.OPTIMAL:
        print('--- Trajeto Ótimo Encontrado ---')
        print(f'Custo Mínimo de Construção: {solver.Objective().Value():.0f}\n')
        
        # Reconstruir o caminho a partir das variáveis
        caminho = ['A']
        no_atual_idx = start_node_idx
        while no_atual_idx != end_node_idx:
            for i, j in x:
                if i == no_atual_idx and x[i, j].solution_value() > 0.9:
                    no_atual_idx = j
                    caminho.append(reverse_node_map[no_atual_idx])
                    break
        
        caminho_formatado = ' -> '.join(caminho)
        print(f'Caminho: {caminho_formatado}')
    else:
        print('Não foi possível encontrar um caminho ótimo.')

if __name__ == '__main__':
    resolver_caminho_minimo_pl()
