from IPython.display import display, Markdown, Latex, Math
import numpy as np
import sympy

class SOLVER:
    """
    Classe que implementa o método Simplex para resolver problemas de Programação Linear.
    Gera tableaux formatados em LaTeX para visualização.
    """
    def __init__(self, tableau):
        self.original_tableau = sympy.Matrix(tableau)
        self.current_tableau = self.original_tableau.copy()
        self.num_rows = self.original_tableau.shape[0]  # Número de linhas
        self.num_cols = self.original_tableau.shape[1]  # Número de colunas
        self.num_vars = self.num_cols - self.num_rows   # Número de variáveis de decisão
        
        # Dicionário para armazenar o estado das variáveis (básicas/não-básicas)
        self.vars = { 
            "X_"+str(i+1): {
                "type": "NB" if i < self.num_vars else "B",  # NB = Não básica, B = Básica
                "value": 0 if i < self.num_vars else tableau[i-self.num_vars+1][-1],
                "row": 0 if i < (self.num_cols-self.num_rows) else i-self.num_vars+1
            } 
            for i in range(self.num_cols-1)
        }
        
        self.lpivo = -1  # Linha do pivô
        self.cpivo = -1  # Coluna do pivô

    def isoptimum(self):
        """Verifica se a solução atual é ótima (quando não há coeficientes negativos na linha Z)"""
        return min(self.current_tableau[0,:]) >= 0

    def pivo(self):
        """Seleciona o elemento pivô usando a regra de Bland"""
        # Encontra a coluna pivô (mais negativo na linha Z)
        self.cpivo = np.argmin(self.current_tableau[0,:])
        
        # Encontra a linha pivô usando a regra da razão mínima
        menor = np.inf
        for lin in range(1, self.num_rows):
            if self.current_tableau[lin, self.cpivo] > 0:
                temp = self.current_tableau[lin, self.num_cols-1] / self.current_tableau[lin, self.cpivo]
                if temp < menor:
                    self.lpivo = lin
                    menor = temp

    def iteration(self):
        """Executa uma iteração completa do método Simplex"""
        TC = self.current_tableau
        LP = self.lpivo
        CP = self.cpivo
        
        # Passo 1: Normaliza a linha do pivô
        TC[LP,:] = TC[LP,:] / TC[LP,CP]
        
        # Passo 2: Zera os outros elementos da coluna pivô
        for i in range(self.num_rows):
            if i != self.lpivo:
                TC[i,:] = TC[i,:] - TC[i,CP] * TC[LP,:]
        
        self.update_dict()

    def update_dict(self):
        """Atualiza o dicionário de variáveis após cada iteração"""
        variables = list(self.vars.keys())
        pos = [self.vars[key]['row'] for key in self.vars.keys()]
        
        # Variável que entra na base
        self.vars[variables[self.cpivo]]['type'] = "B"
        self.vars[variables[self.cpivo]]['value'] = self.current_tableau[self.lpivo,-1]
        self.vars[variables[self.cpivo]]['row'] = self.lpivo
        
        # Variável que sai da base
        exit_var = variables[pos.index(self.lpivo)]
        self.vars[exit_var]['type'] = "NB"
        self.vars[exit_var]['value'] = 0
        self.vars[exit_var]['row'] = 0

    def solver(self):
        """Executa o método Simplex até encontrar a solução ótima"""
        iter = 0
        step = r"$$\begin{matrix}"
        self.current_tableau = self.original_tableau.copy()
        
        while not self.isoptimum():
            step += r"\begin{matrix} " + self.latex_solution()[2:-2] + r"\\ Tableau \\"
            step += self.latex()[2:-2] + r"\\ Pivo \\"
            self.pivo()
            step += solver.latex(pivo=True)[2:-2] + r"\end{matrix} &"
            self.iteration()
            iter += 1
            
        step += self.latex_solution()[2:-2] + r" \\ Tableau \ Final \\"
        step += self.latex()[2:-2]
        step += r"\end{matrix}$$"
        return step

    def latex_solution(self):
        """Gera a representação LaTeX da solução atual"""
        base = []
        notbase = []
        for key, value in self.vars.items():
            if value['type'] == "B":
                base.append(f"{key}={value['value']}")
            else:
                notbase.append(f"{key}={value['value']}")
                
        base = ",".join(base)
        notbase = ",".join(notbase)
        
        solution = r"$$\begin{matrix} Básicas & = & \{"
        solution += base + r"\}\\ Não\ Básicas & = & \{"
        solution += notbase + r"\\ Objetivo & = &"
        solution += str(self.current_tableau[0,-1]) + r"\end{matrix}$$"
        return solution

    def latex(self, leftlabel="", pivo=False):
        """Gera a representação LaTeX do tableau atual"""
        variables = list(self.vars.keys())
        pos = [self.vars[key]['row'] for key in self.vars.keys()]
        
        # Cabeçalho do tableau
        code = r"$$" + leftlabel + r"\left[ \left| \begin{matrix} Vars \\ Z "
        for lin in range(self.num_rows-1):
            var = variables[pos.index(lin+1)]
            if lin + 1 == self.lpivo and pivo:
                code += r'\\ \leftarrow ' + var
            else:
                code += r'\\' + var
                
        code += r'\end{matrix} \right| '
        code += r'\begin{matrix}'
        
        # Nomes das colunas
        for j in range(self.num_cols-1):
            if j == self.cpivo and pivo:
                code += '\downarrow'
            code += ' ' + variables[j] + ' & '
        code += r' b \\'
        
        # Valores do tableau
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if i == self.lpivo and j == self.cpivo and pivo:
                    code += "\\fbox{" + str(self.current_tableau[i,j]) + "}"
                else:
                    code += str(self.current_tableau[i,j])
                code += r' & ' if j < self.num_cols-1 else r'\\'
                
        code += r'\end{matrix} \right]$$'
        return code

    def printmatrix(self):
        """Exibe o tableau formatado no notebook"""
        display(Math(self.latex()))


# Exemplos de uso (problemas de programação linear)
"""### Exercício 01"""
Tableau1 = [
    [-4,-3, 0, 0, 0, 0, 0],
    [ 1, 3, 1, 0, 0, 0, 7],
    [ 2, 2, 0, 1, 0, 0, 8],
    [ 1, 1, 0, 0, 1, 0, 3],
    [ 0, 1, 0, 0, 0, 1, 2]
]
solver1 = SOLVER(Tableau1)
display(Math(solver1.latex()))

solver1.pivo()
display(Math(solver1.latex(pivo=True)))

solver1.iteration()
display(Math(solver1.latex()))

"""### Exercício 02"""
Tableau2 = [
    [-4, -8, 0, 0, 0,  0],
    [ 3,  2, 1, 0, 0, 18],
    [ 1,  1, 0, 1, 0,  5],
    [ 1,  0, 0, 0, 1,  4]
]
solver2 = SOLVER(Tableau2)
display(Math(solver2.latex()))

solver2.pivo()
display(Math(solver2.latex(pivo=True)))
solver2.iteration()
display(Math(solver2.latex()))

"""### Exercício 03"""
Tableau3 = [
    [-2,  1, -1, 0, 0, 0,  0],
    [ 3,  1,  1, 1, 0, 0, 60],
    [ 1, -1,  2, 0, 1, 0, 10],
    [ 1,  1, -1, 0, 0, 1, 20]
]
solver3 = SOLVER(Tableau3)
display(Math(solver3.latex()))

solver3.pivo()
display(Math(solver3.latex(pivo=True)))
solver3.iteration()
display(Math(solver3.latex()))
solver3.pivo()
display(Math(solver3.latex(pivo=True)))
solver3.iteration()
display(Math(solver3.latex()))

"""### Exercício 04"""
Tableau4 = [
    [-16, -6, -15, 0, 0, 0],
    [ 10,  3,   2, 1, 0, 1200],
    [  5,  2,   5, 0, 1, 2000]
]
solver4 = SOLVER(Tableau4)
display(Math(solver4.latex()))

solver4.pivo()
display(Math(solver4.latex(pivo=True)))
solver4.iteration()
display(Math(solver4.latex()))
solver4.pivo()
display(Math(solver4.latex(pivo=True)))
solver4.iteration()
display(Math(solver4.latex()))

"""### Exercício 05"""
Tableau5 = [
    [-5, -4, -3, 0, 0, 0,  0],
    [ 2,  3,  1, 1, 0, 0,  5],
    [ 4,  2,  2, 0, 1, 0, 11],
    [ 3,  2,  2, 0, 0, 1,  8]
]
solver5 = SOLVER(Tableau5)
display(Math(solver5.latex()))

solver5.pivo()
display(Math(solver5.latex(pivo=True)))
solver5.iteration()
display(Math(solver5.latex()))
solver5.pivo()
display(Math(solver5.latex(pivo=True)))
solver5.iteration()
display(Math(solver5.latex()))

