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

\subsection*{Notation}
\begin{itemize}
    \item Let \( K \) be the total number of spare parts.
    \item Let \( S \) be the total number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_k \) be the profit of part \( k \).
    \item Let \( capacity_s \) be the capacity of shop \( s \) in working hours.
    \item Let \( quantity_k \) be the quantity of spare part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The total time used in each shop must not exceed its capacity. For each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \forall s = 1, 2, \ldots, S
\]

Additionally, we require that the quantity produced for each spare part is non-negative:
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\subsection*{Complete Model}
The complete linear programming model can be summarized as follows:

\[
\begin{aligned}
& \text{Maximize} && Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
& \text{subject to} \\
& && \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, 2, \ldots, S \\
& && quantity_k \geq 0, \quad \forall k = 1, 2, \ldots, K 
\end{aligned}
\]

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

\subsection*{Notation}
\begin{itemize}
    \item Let \( K \) be the total number of spare parts.
    \item Let \( S \) be the total number of shops.
    \item Let \( time_{k,s} \) be the required worker-hours for part \( k \) in shop \( s \).
    \item Let \( profit_k \) be the profit of part \( k \).
    \item Let \( capacity_s \) be the capacity of shop \( s \) in working hours.
    \item Let \( quantity_k \) be the quantity of spare part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
We want to maximize the total profit:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The total time used in each shop must not exceed its capacity. For each shop \( s \):
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \forall s = 1, 2, \ldots, S
\]

Additionally, we require that the quantity produced for each spare part is non-negative:
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\subsection*{Complete Model}
The complete linear programming model can be summarized as follows:

\[
\begin{aligned}
& \text{Maximize} && Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
& \text{subject to} \\
& && \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, 2, \ldots, S \\
& && quantity_k \geq 0, \quad \forall k = 1, 2, \ldots, K 
\end{aligned}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}'
data = json.loads(data)

#### Extract data
time = data['time']  #### List of lists
profit = data['profit']
capacity = data['capacity']

K = len(profit)  #### Number of spare parts
S = len(capacity)  #### Number of shops

#### Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]), f"Capacity_Constraint_Shop_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

