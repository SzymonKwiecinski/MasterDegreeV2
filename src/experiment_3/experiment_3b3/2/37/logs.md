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

\section*{Linear Programming Model for Maximizing Profit in Spare Part Production}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for spare parts, where \( k = 1, \ldots, K \)
    \item \( s \): Index for shops, where \( s = 1, \ldots, S \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{k,s} \): Worker-hours required for part \( k \) in shop \( s \)
    \item \( profit_{k} \): Profit obtained from producing part \( k \)
    \item \( capacity_{s} \): Capacity of shop \( s \) in terms of working hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( quantity_{k} \): Quantity of spare part \( k \) to be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\]

\subsection*{Constraints}
The total worker-hours required in each shop must not exceed its capacity:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s \in \{1, \ldots, S\}
\]

Additionally, the quantity of each spare part must be non-negative:
\[
quantity_{k} \geq 0, \quad \forall k \in \{1, \ldots, K\}
\]

\subsection*{Output Format}
The output will provide the optimal quantities of each spare part to be produced:
\[
\text{Output:} \quad quantity = [quantity_{1}, quantity_{2}, \ldots, quantity_{K}]
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

\section*{Linear Programming Model for Maximizing Profit in Spare Part Production}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for spare parts, where \( k = 1, \ldots, K \)
    \item \( s \): Index for shops, where \( s = 1, \ldots, S \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( time_{k,s} \): Worker-hours required for part \( k \) in shop \( s \)
    \item \( profit_{k} \): Profit obtained from producing part \( k \)
    \item \( capacity_{s} \): Capacity of shop \( s \) in terms of working hours
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( quantity_{k} \): Quantity of spare part \( k \) to be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} profit_{k} \cdot quantity_{k}
\]

\subsection*{Constraints}
The total worker-hours required in each shop must not exceed its capacity:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_{k} \leq capacity_{s}, \quad \forall s \in \{1, \ldots, S\}
\]

Additionally, the quantity of each spare part must be non-negative:
\[
quantity_{k} \geq 0, \quad \forall k \in \{1, \ldots, K\}
\]

\subsection*{Output Format}
The output will provide the optimal quantities of each spare part to be produced:
\[
\text{Output:} \quad quantity = [quantity_{1}, quantity_{2}, \ldots, quantity_{K}]
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Unpack data
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of spare parts (K) and shops (S)
K = len(profit)
S = len(capacity)

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K))

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s]

#### Solve the problem
problem.solve()

#### Output the optimal quantities of each spare part to be produced
optimal_quantities = [pulp.value(quantity[k]) for k in range(K)]
print(f'Optimal Quantities: {optimal_quantities}')

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

