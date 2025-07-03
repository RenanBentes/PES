import numpy as np
import sympy

class SOLVER:
    """
    Classe que implementa o método Simplex para resolver problemas de Programação Linear.
    Adaptada para exibir o tableau em um terminal de texto.
    """

    def __init__(self, tableau):
        self.original_tableau = sympy.Matrix(tableau)
        self.current_tableau = self.original_tableau.copy()
        self.num_rows = self.original_tableau.shape[0]
        self.num_cols = self.original_tableau.shape[1]
        self.num_decision_vars = self.num_cols - self.num_rows
        self.pivot_row = -1
        self.pivot_col = -1
        self.variables = {}
        for i in range(self.num_cols - 1):
            if i < self.num_decision_vars:
                var_name = f"x_{i + 1}"
                self.variables[var_name] = {"type": "NB", "row": 0}
            else:
                var_name = f"s_{i - self.num_decision_vars + 1}"
                self.variables[var_name] = {"type": "B", "row": i - self.num_decision_vars + 1}

    def is_optimal(self):
        return all(val >= 0 for val in self.current_tableau[0, :-1])

    def find_pivot(self):
        if self.is_optimal():
            print("Solução ótima já foi encontrada.")
            return False
        self.pivot_col = np.argmin(self.current_tableau[0, :-1])
        min_ratio = float('inf')
        pivot_row_candidate = -1
        for r_idx in range(1, self.num_rows):
            element = self.current_tableau[r_idx, self.pivot_col]
            if element > 0:
                ratio = self.current_tableau[r_idx, -1] / element
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row_candidate = r_idx
        if pivot_row_candidate == -1:
            raise Exception("O problema possui solução ilimitada (unbounded).")
        self.pivot_row = pivot_row_candidate
        return True

    def iterate(self):
        if self.pivot_row == -1 or self.pivot_col == -1:
            print("Nenhum pivô selecionado.")
            return
        tableau = self.current_tableau
        pivot_element = tableau[self.pivot_row, self.pivot_col]
        tableau[self.pivot_row, :] /= pivot_element
        for r_idx in range(self.num_rows):
            if r_idx != self.pivot_row:
                multiplier = tableau[r_idx, self.pivot_col]
                tableau[r_idx, :] -= multiplier * tableau[self.pivot_row, :]
        self._update_variables()

    def _update_variables(self):
        for name, info in self.variables.items():
            if info["type"] == "B" and info["row"] == self.pivot_row:
                self.variables[name]["type"] = "NB"
                self.variables[name]["row"] = 0
                break
        entering_var_name = list(self.variables.keys())[self.pivot_col]
        self.variables[entering_var_name]["type"] = "B"
        self.variables[entering_var_name]["row"] = self.pivot_row

    def display_terminal(self, pivo=False):
        """Exibe o tableau de forma legível em um terminal de texto."""
        print("\n--- Tableau Atual ---")

        # Constrói o cabeçalho
        header = [name for name in self.variables.keys()]
        header.append("b")
        print("Base | " + " | ".join(f"{h:^7}" for h in header))
        print("-" * (len(header) * 11))

        # Constrói as linhas
        base_vars = {info["row"]: name for name, info in self.variables.items() if info["type"] == 'B'}

        for r_idx in range(self.num_rows):
            row_header = "Z" if r_idx == 0 else base_vars.get(r_idx, "?")
            row_str = f"{row_header:^4} | "
            for c_idx in range(self.num_cols):
                element = self.current_tableau[r_idx, c_idx]
                element_str = f"{float(element):7.2f}"
                if pivo and r_idx == self.pivot_row and c_idx == self.pivot_col:
                    element_str = f"[{element_str.strip()}]"  # Destaca o pivô

                row_str += f"{element_str:^7}" + " | "
            print(row_str)
        print("-" * (len(header) * 11))
# --- Exemplos de Uso (a lógica original foi mantida) ---

"""### Exercício 01"""
print("--- Exercício 01: Início ---")
Tableau1 = [[-4, -3, 0, 0, 0, 0, 0], [1, 3, 1, 0, 0, 0, 7], [2, 2, 0, 1, 0, 0, 8], [1, 1, 0, 0, 1, 0, 3],
            [0, 1, 0, 0, 0, 1, 2]]
solver1 = SOLVER(Tableau1)
solver1.display_terminal()
solver1.find_pivot()
solver1.iterate()
solver1.display_terminal()
print("--- Exercício 01: Fim ---\n")

"""### Exercício 02"""
print("--- Exercício 02: Início ---")
Tableau2 = [[-4, -8, 0, 0, 0, 0], [3, 2, 1, 0, 0, 18], [1, 1, 0, 1, 0, 5], [1, 0, 0, 0, 1, 4]]
solver2 = SOLVER(Tableau2)
solver2.display_terminal()
solver2.find_pivot()
solver2.iterate()
solver2.display_terminal()
print("--- Exercício 02: Fim ---\n")

"""### Exercício 03"""
print("--- Exercício 03: Início ---")
Tableau3 = [[-2, 1, -1, 0, 0, 0, 0], [3, 1, 1, 1, 0, 0, 60], [1, -1, 2, 0, 1, 0, 10], [1, 1, -1, 0, 0, 1, 20]]
solver3 = SOLVER(Tableau3)
solver3.display_terminal()
solver3.find_pivot()
solver3.iterate()
solver3.display_terminal()
solver3.find_pivot()
solver3.iterate()
solver3.display_terminal()
print("--- Exercício 03: Fim ---\n")

"""### Exercício 04"""
print("--- Exercício 04: Início ---")
Tableau4 = [[-16, -6, -15, 0, 0, 0], [10, 3, 2, 1, 0, 1200], [5, 2, 5, 0, 1, 2000]]
solver4 = SOLVER(Tableau4)
solver4.display_terminal()
solver4.find_pivot()
solver4.iterate()
solver4.display_terminal()
solver4.find_pivot()
solver4.display_terminal()
solver4.iterate()
solver4.display_terminal()
print("--- Exercício 04: Fim ---\n")

"""### Exercício 05"""
print("--- Exercício 05: Início ---")
Tableau5 = [[-5, -4, -3, 0, 0, 0, 0], [2, 3, 1, 1, 0, 0, 5], [4, 2, 2, 0, 1, 0, 11], [3, 2, 2, 0, 0, 1, 8]]
solver5 = SOLVER(Tableau5)
solver5.display_terminal()
solver5.find_pivot()
solver5.iterate()
solver5.display_terminal()
solver5.find_pivot()
solver5.iterate()
solver5.display_terminal()
print("--- Exercício 05: Fim ---\n")