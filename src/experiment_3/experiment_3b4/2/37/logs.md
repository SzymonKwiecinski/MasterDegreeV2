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
To formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit, we can model it as a Linear Programming (LP) problem. The decision variables will represent the quantity of each part to be produced, and the objective is to maximize the total profit subject to the constraints imposed by the shop capacities.

Let's denote:
- \( x_k \): the quantity of part \( k \) to be produced.
- \( \text{profit}_k \): the profit for each unit of part \( k \).
- \( \text{time}_{k,s} \): the worker-hours required for part \( k \) in shop \( s \).
- \( \text{capacity}_s \): the capacity of shop \( s \) in worker-hours.

The linear programming formulation is as follows:

**Objective Function:**
The objective is to maximize the total profit:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

**Subject to Constraints:**
1. Capacity constraints for each shop \( s \):
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s \quad \text{for all } s = 1, \ldots, S
\]

2. Non-negativity constraints for the quantities:
\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

Now, we can represent this formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Maximizing Profit}

Let:
\begin{align*}
x_k & : \text{the quantity of part } k \text{ to be produced}, \\
\text{profit}_k & : \text{the profit for each unit of part } k, \\
\text{time}_{k,s} & : \text{the worker-hours required for part } k \text{ in shop } s, \\
\text{capacity}_s & : \text{the capacity of shop } s \text{ in worker-hours}.
\end{align*}

Objective:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

Subject to:
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s \quad \text{for all } s = 1, \ldots, S
\]

\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
\]

\end{document}
``` 

This formulation will allow us to determine the optimal number of each type of spare part to produce in order to maximize the firm's profit, given the constraints of shop capacities.

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

Let:
\begin{align*}
x_k & : \text{the quantity of part } k \text{ to be produced}, \\
\text{profit}_k & : \text{the profit for each unit of part } k, \\
\text{time}_{k,s} & : \text{the worker-hours required for part } k \text{ in shop } s, \\
\text{capacity}_s & : \text{the capacity of shop } s \text{ in worker-hours}.
\end{align*}

Objective:
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

Subject to:
\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s \quad \text{for all } s = 1, \ldots, S
\]

\[
x_k \geq 0 \quad \text{for all } k = 1, \ldots, K
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

time = data['time']
profit = data['profit']
capacity = data['capacity']

num_parts = len(profit)
num_shops = len(capacity)

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(num_parts)]

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(num_parts))

#### Constraints
for s in range(num_shops):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(num_parts)) <= capacity[s], f"Capacity_Constraint_Shop_{s+1}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

