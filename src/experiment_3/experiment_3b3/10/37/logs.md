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

\section*{Linear Programming Model for Maximizing Profit in Spare Automobile Parts Production}

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for spare parts, where $k = 1, 2, \ldots, K$
    \item $s$: Index for shops, where $s = 1, 2, \ldots, S$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{k,s}$: Required worker-hours for part $k$ in shop $s$
    \item $profit_k$: Profit of part $k$
    \item $capacity_s$: Capacity of shop $s$ in working hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $quantity_k$: Quantity of spare part $k$ to be produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \forall s = 1, 2, \ldots, S
\]
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
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

\section*{Linear Programming Model for Maximizing Profit in Spare Automobile Parts Production}

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for spare parts, where $k = 1, 2, \ldots, K$
    \item $s$: Index for shops, where $s = 1, 2, \ldots, S$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{k,s}$: Required worker-hours for part $k$ in shop $s$
    \item $profit_k$: Profit of part $k$
    \item $capacity_s$: Capacity of shop $s$ in working hours
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $quantity_k$: Quantity of spare part $k$ to be produced
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s \quad \forall s = 1, 2, \ldots, S
\]
\[
quantity_k \geq 0 \quad \forall k = 1, 2, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of parts and shops
K = len(profit)
S = len(capacity)

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

