import pulp as plp

def continuous_optimization():
    print("\n=== Continuous Variables Optimization ===")
    model = plp.LpProblem('MRPInverso_Continuous', plp.LpMaximize)
    X1 = plp.LpVariable('X1', lowBound=0, cat=plp.LpContinuous)
    X2 = plp.LpVariable('X2', lowBound=0, cat=plp.LpContinuous)
    
    # Constraints
    model += 100*X1 + 150*X2, "Maximize_Profit"
    model += X1 + X2 <= 10, "Board_Constraint"
    model += X1 + 2*X2 <= 12, "Memory_Constraint"
    print(model)
    model.solve()
    
    # Results
    print("\nOptimal Solution:")
    for var in model.variables():
        print(f"{var.name} = {var.varValue}")
    print(f"Optimal Value: {plp.value(model.objective)}\n")

def integer_optimization():
    print("\n=== Integer Variables Optimization ===")
    model = plp.LpProblem('MRPInverso_Integer', plp.LpMaximize)
    X1 = plp.LpVariable('X1', lowBound=0, cat=plp.LpInteger)
    X2 = plp.LpVariable('X2', lowBound=0, cat=plp.LpInteger)
    model += 100*X1 + 150*X2, "Maximize_Profit"
    
    # Constraints
    model += X1 + X2 <= 10, "Board_Constraint"
    model += X1 + 2*X2 <= 12, "Memory_Constraint"
    model += 48*X1 + 60*X2 <= 480, "Hours_Constraint"
    model.solve()
    
    # Results
    print("\nOptimal Solution:")
    for var in model.variables():
        print(f"{var.name} = {var.varValue}")
    print(f"Optimal Value: {plp.value(model.objective)}\n")

def shortest_path_problem():
    print("\n=== Shortest Path Optimization ===")
    # Data
    arc_names = ["X1", "X2", "X3", "X4", "X5", "X6", "X7"]
    distances = [41, 50, 44, 37, 27, 45, 4]
    incidence_matrix = [
        [1, 1, 1,  0,  0,  0,  0],
        [1, 0, 0, -1,  0,  0,  0],
        [0, 0, 1,  0, -1,  0,  0],
        [0, 0, 0,  1,  0, -1,  0],
        [0, 1, 0,  0,  1,  0, -1],
        [0, 0, 0,  0,  0,  1,  1]
    ]
    node_balance = [1, 0, 0, 0, 0, 1]
    cities = ["Lambari", "Três Corações", "São Lourenço", 
             "São Thomé das Letras", "Caxambu", "Baependi"]
    model = plp.LpProblem("Shortest_Path", plp.LpMinimize)
    variables = [plp.LpVariable(name, cat=plp.LpBinary) for name in arc_names]

    model += plp.lpSum(distances[i]*variables[i] for i in range(len(arc_names))), 'Total_Distance'

    for node_idx, city in enumerate(cities):
        constraint = plp.lpSum(
            incidence_matrix[node_idx][i] * variables[i] 
            for i in range(len(arc_names))
        ) == node_balance[node_idx]
        model += constraint, f"Node_Balance_{city}"

    status = model.solve()

    print("\nOptimal Path:")
    for var in model.variables():
        if var.varValue > 0.9:  
            print(f"{var.name} = {var.varValue}")
    print(f"\nMinimum Distance: {plp.value(model.objective)}")
    print(f"Solver Status: {plp.LpStatus[status]}")

if __name__ == "__main__":
    continuous_optimization()
    integer_optimization()
    shortest_path_problem()
