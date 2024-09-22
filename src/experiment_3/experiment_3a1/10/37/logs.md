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

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $K$ = Number of spare parts
    \item $S$ = Number of shops
    \item $time_{k,s}$ = Required worker-hours for part $k$ in shop $s$
    \item $profit_k$ = Profit from part $k$
    \item $capacity_s$ = Capacity of shop $s$ in working hours
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $quantity_k$ = Quantity of spare part $k$ to be produced for $k = 1, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit, which can be formulated as:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The constraints for the problem are based on the capacities of the shops:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The decision variables must be non-negative:
\[
quantity_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Complete Model}
Combining the objective function and constraints, the complete linear programming model can be expressed as:

\[
\begin{align*}
    & \text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
    & \text{subject to} \\
    & \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S \\
    & quantity_k \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}
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

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $K$ = Number of spare parts
    \item $S$ = Number of shops
    \item $time_{k,s}$ = Required worker-hours for part $k$ in shop $s$
    \item $profit_k$ = Profit from part $k$
    \item $capacity_s$ = Capacity of shop $s$ in working hours
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item $quantity_k$ = Quantity of spare part $k$ to be produced for $k = 1, \ldots, K$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit, which can be formulated as:
\[
\text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k
\]

\subsection*{Constraints}
The constraints for the problem are based on the capacities of the shops:
\[
\sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S
\]

\subsection*{Non-negativity Constraints}
The decision variables must be non-negative:
\[
quantity_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\subsection*{Complete Model}
Combining the objective function and constraints, the complete linear programming model can be expressed as:

\[
\begin{align*}
    & \text{Maximize } Z = \sum_{k=1}^{K} profit_k \cdot quantity_k \\
    & \text{subject to} \\
    & \sum_{k=1}^{K} time_{k,s} \cdot quantity_k \leq capacity_s, \quad \forall s = 1, \ldots, S \\
    & quantity_k \geq 0, \quad \forall k = 1, \ldots, K
\end{align*}
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from the provided JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Define problem
K = len(data['profit'])  #### Number of spare parts
S = len(data['capacity'])  #### Number of shops

#### Create the linear programming problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

#### Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

#### Objective function
problem += pulp.lpSum(data['profit'][k] * quantity[k] for k in range(K)), "Total Profit"

#### Constraints
for s in range(S):
    problem += (pulp.lpSum(data['time'][k][s] * quantity[k] for k in range(K)) <= data['capacity'][s]), f"Capacity_Constraint_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

