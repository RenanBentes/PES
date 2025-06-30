import pulp


# --------------------------------------------------------------------------
# Problema 1: Rota Mínima (Chapecó → Porto Alegre)
# --------------------------------------------------------------------------
def resolver_rota_minima():
    """Resolve o problema de encontrar o caminho mais curto em uma rede."""
    print("--- Resolvendo Problema 1: Rota Mínima ---")

    # 1. Definir o modelo de minimização
    modelo = pulp.LpProblem("Rota_Minima_Chapecó_POA", pulp.LpMinimize)

    # 2. Dados: trechos e suas distâncias
    trechos = {
        ("Chapecó", "Joaçaba"): 400, ("Chapecó", "Lages"): 950, ("Chapecó", "Joinville"): 800,
        ("Joaçaba", "Caxias do Sul"): 1800, ("Joaçaba", "Florianópolis"): 900,
        ("Lages", "Florianópolis"): 1100,
        ("Joinville", "Florianópolis"): 600, ("Joinville", "Sombrio"): 1200,
        ("Caxias do Sul", "Florianópolis"): 900, ("Caxias do Sul", "Porto Alegre"): 400,
        ("Florianópolis", "Porto Alegre"): 1300, ("Florianópolis", "Sombrio"): 1000,
        ("Sombrio", "Porto Alegre"): 600
    }

    cidades = ["Chapecó", "Joaçaba", "Lages", "Joinville", "Caxias do Sul", "Florianópolis", "Sombrio", "Porto Alegre"]

    # 3. Variáveis: x_ij = 1 se o trecho (i,j) for usado, 0 caso contrário
    vars_trechos = pulp.LpVariable.dicts("Rota", trechos.keys(), cat='Binary')

    # 4. Função Objetivo: Minimizar a distância total
    modelo += pulp.lpSum([distancia * vars_trechos[trecho] for trecho, distancia in trechos.items()]), "Distancia_Total"

    # 5. Restrições de fluxo para garantir um caminho contínuo
    for cidade in cidades:
        fluxo_saida = pulp.lpSum([vars_trechos[c, j] for c, j in trechos if c == cidade])
        fluxo_entrada = pulp.lpSum([vars_trechos[i, c] for i, c in trechos if c == cidade])

        if cidade == "Chapecó":
            modelo += fluxo_saida - fluxo_entrada == 1, f"Fluxo_{cidade}"
        elif cidade == "Porto Alegre":
            modelo += fluxo_saida - fluxo_entrada == -1, f"Fluxo_{cidade}"
        else:
            modelo += fluxo_saida - fluxo_entrada == 0, f"Fluxo_{cidade}"

    # 6. Resolver e imprimir o resultado
    modelo.solve()
    print(f"Status: {pulp.LpStatus[modelo.status]}")
    if pulp.LpStatus[modelo.status] == 'Optimal':
        distancia_total = pulp.value(modelo.objective)
        print(f"Distância Mínima: {distancia_total} km")
        print("Rota a seguir:")
        for trecho in trechos:
            if vars_trechos[trecho].varValue == 1:
                print(f"  De {trecho[0]} para {trecho[1]}")


# --------------------------------------------------------------------------
# Problema 2: Fluxo Máximo de Energia (Chapecó → Porto Alegre)
# --------------------------------------------------------------------------
def resolver_fluxo_maximo_energia():
    """Resolve o problema de encontrar o fluxo máximo em uma rede."""
    print("--- Resolvendo Problema 2: Fluxo Máximo de Energia ---")

    modelo = pulp.LpProblem("Fluxo_Maximo_Energia", pulp.LpMaximize)

    # Dados: trechos (eletrovias) e suas capacidades
    capacidades = {
        ("Chapecó", "Joaçaba"): 400, ("Chapecó", "Lages"): 950, ("Chapecó", "Joinville"): 800,
        ("Joaçaba", "Caxias do Sul"): 1800, ("Joaçaba", "Florianópolis"): 900,
        ("Lages", "Florianópolis"): 1100,
        ("Joinville", "Florianópolis"): 600, ("Joinville", "Sombrio"): 1200,
        ("Caxias do Sul", "Florianópolis"): 900, ("Caxias do Sul", "Porto Alegre"): 400,
        ("Florianópolis", "Porto Alegre"): 1300, ("Florianópolis", "Sombrio"): 1000,
        ("Sombrio", "Porto Alegre"): 600
    }
    cidades = ["Chapecó", "Joaçaba", "Lages", "Joinville", "Caxias do Sul", "Florianópolis", "Sombrio", "Porto Alegre"]

    # Variáveis: f_ij, fluxo no trecho (i,j)
    vars_fluxo = pulp.LpVariable.dicts("Fluxo", capacidades.keys(), lowBound=0)

    # Função Objetivo: Maximizar o fluxo que sai de Chapecó
    modelo += pulp.lpSum([vars_fluxo[c, j] for c, j in capacidades if c == "Chapecó"]), "Fluxo_Total_Saida"

    # Restrições de capacidade de cada trecho
    for trecho, cap in capacidades.items():
        modelo += vars_fluxo[trecho] <= cap, f"Capacidade_{trecho[0]}_{trecho[1]}"

    # Restrições de conservação de fluxo para nós intermediários
    for cidade in cidades:
        if cidade not in ["Chapecó", "Porto Alegre"]:
            fluxo_entrada = pulp.lpSum([vars_fluxo[i, c] for i, c in capacidades if c == cidade])
            fluxo_saida = pulp.lpSum([vars_fluxo[c, j] for c, j in capacidades if c == cidade])
            modelo += fluxo_entrada == fluxo_saida, f"Conservacao_{cidade}"

    modelo.solve()
    print(f"Status: {pulp.LpStatus[modelo.status]}")
    if pulp.LpStatus[modelo.status] == 'Optimal':
        fluxo_total = pulp.value(modelo.objective)
        print(f"Fluxo Máximo de Energia: {fluxo_total} milhões de kw/hora")


# --------------------------------------------------------------------------
# Problema 3: Planejamento de Produção (Aracne S/A)
# --------------------------------------------------------------------------
def resolver_planejamento_producao():
    """Resolve o problema de planejamento de produção multperíodo."""
    print("--- Resolvendo Problema 3: Planejamento de Produção ---")

    modelo = pulp.LpProblem("Planejamento_Aracne", pulp.LpMinimize)
    meses = [1, 2, 3, 4]

    # Dados do problema
    demanda = {1: 420, 2: 580, 3: 310, 4: 540}
    custo_prod = {1: 49, 2: 45, 3: 46, 4: 47}
    cap_prod = {1: 500, 2: 470, 3: 300, 4: 450}
    cap_extra = {1: 50, 2: 60, 3: 45, 4: 20}
    custo_extra = {m: c + 10 for m, c in custo_prod.items()}
    custo_estoque = 1.50
    demanda_min_producao = 300

    # Variáveis
    Pn = pulp.LpVariable.dicts("ProdNormal", meses, lowBound=0, cat='Integer')
    Pe = pulp.LpVariable.dicts("ProdExtra", meses, lowBound=0, cat='Integer')
    S = pulp.LpVariable.dicts("Estoque", [0, 1, 2, 3, 4], lowBound=0, cat='Integer')

    # Restrição: estoque inicial é zero
    modelo += S[0] == 0, "Estoque_Inicial"

    # Função Objetivo: Minimizar custos totais
    custo_total = pulp.lpSum([
        custo_prod[i] * Pn[i] +
        custo_extra[i] * Pe[i] +
        custo_estoque * S[i] for i in meses
    ])
    modelo += custo_total, "Custo_Total"

    # Restrições para cada mês
    for i in meses:
        # Balanço de estoque: Estoque_Anterior + Produção_Total = Demanda + Estoque_Atual
        modelo += S[i - 1] + Pn[i] + Pe[i] - demanda[i] == S[i], f"Estoque_Mes_{i}"
        # Capacidade de produção
        modelo += Pn[i] <= cap_prod[i], f"Capacidade_Normal_Mes_{i}"
        modelo += Pe[i] <= cap_extra[i], f"Capacidade_Extra_Mes_{i}"
        # Produzir pelo menos 300 unidades (conforme o texto)
        modelo += Pn[i] + Pe[i] >= demanda_min_producao, f"Producao_Minima_Mes_{i}"

    modelo.solve()
    print(f"Status: {pulp.LpStatus[modelo.status]}")
    if pulp.LpStatus[modelo.status] == 'Optimal':
        print(f"Custo Total Mínimo: R$ {pulp.value(modelo.objective):.2f}")
        for i in meses:
            print(
                f"  Mês {i}: Prod. Normal={int(Pn[i].varValue)}, Prod. Extra={int(Pe[i].varValue)}, Estoque Final={int(S[i].varValue)}")


# --------------------------------------------------------------------------
# Problema 4: Fluxo Máximo de Óleo (Oleobrás)
# --------------------------------------------------------------------------
def resolver_fluxo_maximo_oleo():
    """Resolve o problema de fluxo máximo de óleo em um oleoduto."""
    print("--- Resolvendo Problema 4: Fluxo Máximo de Óleo ---")

    modelo = pulp.LpProblem("Fluxo_Maximo_Oleo", pulp.LpMaximize)

    # Dados: Estações e capacidades máximas
    capacidades = {
        ("C", "1"): 8, ("C", "2"): 10,
        ("1", "3"): 2, ("1", "4"): 6,
        ("2", "4"): 4, ("2", "5"): 3,
        ("3", "6"): 6, ("3", "R"): 7,
        ("4", "6"): 6, ("4", "R"): 12,
        ("5", "4"): 5
    }
    nos = ["C", "1", "2", "3", "4", "5", "6", "R"]

    vars_fluxo = pulp.LpVariable.dicts("FluxoOleo", capacidades.keys(), lowBound=0)

    # Objetivo: Maximizar fluxo que sai de C
    modelo += pulp.lpSum([vars_fluxo[c, j] for c, j in capacidades if c == "C"]), "Fluxo_Total_Oleo"

    # Restrições de capacidade
    for trecho, cap in capacidades.items():
        modelo += vars_fluxo[trecho] <= cap, f"Capacidade_Oleo_{trecho[0]}_{trecho[1]}"

    # Restrições de conservação de fluxo para nós intermediários
    for no in nos:
        if no not in ["C", "R"]:
            fluxo_entrada = pulp.lpSum([vars_fluxo[i, c] for i, c in capacidades if c == no])
            fluxo_saida = pulp.lpSum([vars_fluxo[c, j] for c, j in capacidades if c == no])
            modelo += fluxo_entrada == fluxo_saida, f"Conservacao_Oleo_{no}"

    modelo.solve()
    print(f"Status: {pulp.LpStatus[modelo.status]}")
    if pulp.LpStatus[modelo.status] == 'Optimal':
        print(f"Fluxo Máximo de Óleo: {pulp.value(modelo.objective)}")


# --------------------------------------------------------------------------
# Problema 5: Custo de Transporte (Ego Trip S.A.)
# --------------------------------------------------------------------------
def resolver_transporte():
    """Resolve o problema de minimização de custo de transporte com transbordo."""
    print("--- Resolvendo Problema 5: Custo de Transporte ---")

    modelo = pulp.LpProblem("Custo_Transporte_EgoTrip", pulp.LpMinimize)

    # Nós da rede: Origens, Transbordos, Destinos
    origens = ["SP", "RJ"]
    destinos = ["BSB", "SAL"]
    transbordos = ["VIT", "BH"]

    # Dados de custos
    custos = {
        ("SP", "VIT"): 9, ("SP", "BH"): 12, ("SP", "BSB"): 20, ("SP", "SAL"): 29,
        ("RJ", "VIT"): 14, ("RJ", "BH"): 13, ("RJ", "BSB"): 22, ("RJ", "SAL"): 27,
        ("VIT", "BH"): 5, ("VIT", "BSB"): 18, ("VIT", "SAL"): 18,
        ("BH", "VIT"): 7, ("BH", "BSB"): 16, ("BH", "SAL"): 17
    }

    # Capacidades e Demandas
    capacidade = {"SP": 150, "RJ": 200}
    demanda = {"BSB": 130, "SAL": 130}

    # Variáveis: x_ij, quantidade transportada de i para j
    vars_rotas = pulp.LpVariable.dicts("Transporte", custos.keys(), lowBound=0, cat='Integer')

    # Função Objetivo: Minimizar custo total
    modelo += pulp.lpSum([custos[rota] * vars_rotas[rota] for rota in custos]), "Custo_Total_Transporte"

    # Restrições de capacidade das fábricas (origens)
    for o in origens:
        modelo += pulp.lpSum([vars_rotas[i, j] for i, j in custos if i == o]) <= capacidade[o], f"Capacidade_{o}"

    # Restrições de demanda dos distribuidores (destinos)
    for d in destinos:
        modelo += pulp.lpSum([vars_rotas[i, j] for i, j in custos if j == d]) == demanda[d], f"Demanda_{d}"

    # Restrições de balanço dos nós de transbordo
    for t in transbordos:
        fluxo_entrada = pulp.lpSum([vars_rotas[i, j] for i, j in custos if j == t])
        fluxo_saida = pulp.lpSum([vars_rotas[i, j] for i, j in custos if i == t])
        modelo += fluxo_entrada == fluxo_saida, f"Balanco_{t}"

    modelo.solve()
    print(f"Status: {pulp.LpStatus[modelo.status]}")
    if pulp.LpStatus[modelo.status] == 'Optimal':
        print(f"Custo Mínimo de Transporte: R$ {pulp.value(modelo.objective):.2f}")
        print("Plano de envio:")
        for rota in custos:
            if vars_rotas[rota].varValue > 0:
                print(f"  De {rota[0]} para {rota[1]}: {int(vars_rotas[rota].varValue)} unidades")


# --------------------------------------------------------------------------
# Bloco de Execução Principal
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # Executa a solução para cada um dos 5 problemas em sequência

    resolver_rota_minima()
    print("\n" + "=" * 60 + "\n")

    resolver_fluxo_maximo_energia()
    print("\n" + "=" * 60 + "\n")

    resolver_planejamento_producao()
    print("\n" + "=" * 60 + "\n")

    resolver_fluxo_maximo_oleo()
    print("\n" + "=" * 60 + "\n")

    resolver_transporte()