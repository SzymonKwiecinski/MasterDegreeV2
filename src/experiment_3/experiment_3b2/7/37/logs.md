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
To formulate the described problem as a linear programming model, we need to define decision variables, an objective function, and constraints.

1. **Decision Variables**:  
   Let \( x_k \) be the quantity of spare part \( k \) to be produced, where \( k = 1, 2, \ldots, K \).

2. **Objective Function**:  
   We aim to maximize the total profit from producing these parts. The objective function can be expressed as:
   \[
   \text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
   \]
   where \( \text{profit}_k \) is the profit per unit of part \( k \).

3. **Constraints**:  
   Each shop \( s \) has a limited capacity of \( \text{capacity}_s \) worker-hours. Thus, for each shop \( s \), the constraint is:
   \[
   \sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s \quad \text{for } s = 1, 2, \ldots, S
   \]
   Additionally, the quantity of each part \( x_k \) must be non-negative:
   \[
   x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
   \]

Below is the formulation of this Linear Programming problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be produced, where \( k = 1, 2, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
The constraints for the shop capacities are given by:
\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s \quad \text{for } s = 1, 2, \ldots, S
\]

Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

\end{document}
```

This LaTeX document provides the mathematical model for the problem of determining the quantities of each spare part to be made during the month to maximize profit, subject to the capacity constraints of each shop.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_k \) be the quantity of spare part \( k \) to be produced, where \( k = 1, 2, \ldots, K \).

\subsection*{Objective Function}
Maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\subsection*{Constraints}
The constraints for the shop capacities are given by:
\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_s \quad \text{for } s = 1, 2, \ldots, S
\]

Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data extraction
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

#### Parameters
K = len(data['profit'])  #### Number of spare parts
S = len(data['capacity'])  #### Number of shop capacities
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

