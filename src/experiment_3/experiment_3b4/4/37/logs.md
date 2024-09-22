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
To formulate the problem as a Linear Programming (LP) model, we aim to determine the quantities of each spare part to be produced such that the total profit is maximized, subject to shop capacity constraints. Let the decision variables be \( x_k \), representing the quantity of spare part \( k \) to be produced.

Given:
- \( \text{time}_{k, s} \): Worker-hours required for part \( k \) in shop \( s \).
- \( \text{profit}_{k} \): Profit for each part \( k \).
- \( \text{capacity}_{s} \): Capacity in working hours of shop \( s \).

The LP model can be formulated as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit.

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
\]
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

Where:
- \( Z \) is the total profit.
- \( x_k \) is the decision variable representing the quantity of part \( k \) to be produced.
- The first set of constraints ensures that the total production hours do not exceed the capacity of each shop.
- The non-negativity constraints ensure that production quantities are not negative.

This LP model essentially determines the optimal production plan (quantities of each spare part) that maximizes profit while respecting the shop capacity constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Maximize the total profit.

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
\]
\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Number of products (K)
K = len(data['profit'])

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * x[k] for k in range(K))

#### Constraints
S = len(data['capacity'])  #### Number of resources

for s in range(S):
    problem += pulp.lpSum(data['time'][k][s] * x[k] for k in range(K)) <= data['capacity'][s]

#### Solve the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

