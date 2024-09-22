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

\section*{Linear Programming Model for Maximizing Profit in Spare Parts Production}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of spare parts.
    \item Let \( S \) be the number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_k \) be the profit for part \( k \).
    \item Let \( capacity_s \) be the capacity of shop \( s \) in working hours.
\end{itemize}

\subsection*{Decision Variables}
Let \( quantity_k \) be the quantity of part \( k \) to be produced, for \( k = 1, \ldots, K \).

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The production in each shop must not exceed its capacity. For each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \text{for } s = 1, \ldots, S
\]

Additionally, the quantities produced must be non-negative:
\[
quantity_k \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Final Model}
Thus, the complete linear programming model can be summarized as follows:
\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
\text{subject to} & \quad \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S \\
& \quad quantity_k \geq 0, \quad \forall k = 1, \ldots, K
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

\section*{Linear Programming Model for Maximizing Profit in Spare Parts Production}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of spare parts.
    \item Let \( S \) be the number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_k \) be the profit for part \( k \).
    \item Let \( capacity_s \) be the capacity of shop \( s \) in working hours.
\end{itemize}

\subsection*{Decision Variables}
Let \( quantity_k \) be the quantity of part \( k \) to be produced, for \( k = 1, \ldots, K \).

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The production in each shop must not exceed its capacity. For each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \text{for } s = 1, \ldots, S
\]

Additionally, the quantities produced must be non-negative:
\[
quantity_k \geq 0, \quad \text{for } k = 1, \ldots, K
\]

\subsection*{Final Model}
Thus, the complete linear programming model can be summarized as follows:
\begin{align*}
\text{Maximize} & \quad Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
\text{subject to} & \quad \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S \\
& \quad quantity_k \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumParts': 5, 'NumMachines': 2, 'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'Profit': [30, 20, 40, 25, 10], 'Capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '''{
    "NumParts": 5,
    "NumMachines": 2,
    "Time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    "Profit": [30, 20, 40, 25, 10],
    "Capacity": [700, 1000]
}'''

#### Parse the data
data_dict = json.loads(data)

#### Parameters
K = data_dict['NumParts']
S = data_dict['NumMachines']
time = data_dict['Time']
profit = data_dict['Profit']
capacity = data_dict['Capacity']

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

