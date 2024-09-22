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

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of different spare parts.
    \item Let \( S \) be the number of shops.
    \item \( \text{time}_{k,s} \): the required worker-hours for part \( k \) in shop \( s \).
    \item \( \text{profit}_{k} \): the profit obtained from part \( k \).
    \item \( \text{capacity}_{s} \): the capacity of shop \( s \) in working hours.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{quantity}_{k} \) be the quantity of spare part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The total worker-hours required for each shop should not exceed the shop's capacity. This can be formulated as follows:
\[
\text{subject to} \quad \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1,2,\ldots,S
\]

Additionally, the quantities of the spare parts must be non-negative:
\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1,2,\ldots,K
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

\section*{Linear Programming Model for Maximizing Profit}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( K \) be the number of different spare parts.
    \item Let \( S \) be the number of shops.
    \item \( \text{time}_{k,s} \): the required worker-hours for part \( k \) in shop \( s \).
    \item \( \text{profit}_{k} \): the profit obtained from part \( k \).
    \item \( \text{capacity}_{s} \): the capacity of shop \( s \) in working hours.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( \text{quantity}_{k} \) be the quantity of spare part \( k \) to be produced.
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{quantity}_{k}
\]

\subsection*{Constraints}
The total worker-hours required for each shop should not exceed the shop's capacity. This can be formulated as follows:
\[
\text{subject to} \quad \sum_{k=1}^{K} \text{time}_{k,s} \cdot \text{quantity}_{k} \leq \text{capacity}_{s}, \quad \forall s = 1,2,\ldots,S
\]

Additionally, the quantities of the spare parts must be non-negative:
\[
\text{quantity}_{k} \geq 0, \quad \forall k = 1,2,\ldots,K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

#### Parameters
time = data['time']  #### time[k][s] for worker-hours
profit = data['profit']  #### profit[k]
capacity = data['capacity']  #### capacity[s]

K = len(profit)  #### Number of spare parts
S = len(capacity)  #### Number of shops

#### Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

#### Objective Function: Maximize total profit
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints: Shop capacity
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

