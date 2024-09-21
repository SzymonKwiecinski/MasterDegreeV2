# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $NumParts$: Number of spare parts to be produced
    \item $NumMachines$: Number of machines available
    \item $Time_{ks}$: Time taken to make one unit of spare part $k$ on machine $s$, for $k = 1, 2, \ldots, NumParts$ and $s = 1, 2, \ldots, NumMachines$
    \item $Profit_k$: Profit from producing one unit of spare part $k$, for $k = 1, 2, \ldots, NumParts$
    \item $Capacity_s$: Capacity of machine $s$ for the month, for $s = 1, 2, \ldots, NumMachines$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_k$: Quantity of spare part $k$ to be produced, for $k = 1, 2, \ldots, NumParts$
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit from the production of spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{NumParts} Profit_k \cdot x_k
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraints for the quantity of each spare part:
    \[
    x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, NumParts
    \]
    \item Machine capacity constraints:
    \[
    \sum_{k=1}^{NumParts} Time_{ks} \cdot x_k \leq Capacity_s \quad \text{for } s = 1, 2, \ldots, NumMachines
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumParts'])]

#### Objective Function
problem += pulp.lpSum([data['Profit'][k] * x[k] for k in range(data['NumParts'])])

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum([data['Time'][k][s] * x[k] for k in range(data['NumParts'])]) <= data['Capacity'][s]

#### Solve the problem
problem.solve()

#### Output the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

