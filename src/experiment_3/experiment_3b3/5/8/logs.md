# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Automobile Parts Production}

\subsection*{Definitions}
\begin{itemize}
    \item Let \( K \) be the total number of spare parts.
    \item Let \( S \) be the total number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_{k} \) be the profit of part \( k \).
    \item Let \( capacity_{s} \) be the capacity of shop \( s \) in working hours.
    \item Let \( quantity_{k} \) be the quantity of part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit from producing spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\]

\subsection*{Constraints}
The production of spare parts must satisfy the capacity constraints of each shop:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s = 1, \ldots, S
\]
Also, we must ensure that the quantity produced for each part is non-negative:
\[
quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Complete Mathematical Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k} \\
\text{Subject to} \quad & \sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s = 1, \ldots, S \\
& quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Spare Automobile Parts Production}

\subsection*{Definitions}
\begin{itemize}
    \item Let \( K \) be the total number of spare parts.
    \item Let \( S \) be the total number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_{k} \) be the profit of part \( k \).
    \item Let \( capacity_{s} \) be the capacity of shop \( s \) in working hours.
    \item Let \( quantity_{k} \) be the quantity of part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit from producing spare parts:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\]

\subsection*{Constraints}
The production of spare parts must satisfy the capacity constraints of each shop:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s = 1, \ldots, S
\]
Also, we must ensure that the quantity produced for each part is non-negative:
\[
quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Complete Mathematical Model}
The complete linear programming model can be summarized as follows:

\begin{align*}
\text{Maximize} \quad & Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k} \\
\text{Subject to} \quad & \sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s = 1, \ldots, S \\
& quantity_{k} \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

#### Unpack data
K = data['NumParts']
S = data['NumMachines']
time = data['Time']
profit = data['Profit']
capacity = data['Capacity']

#### Initialize the problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

