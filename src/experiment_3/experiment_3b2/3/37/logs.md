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
To formulate the given problem as a Linear Programming (LP) model, we need to define the objective function and constraints based on the description provided. The problem aims to maximize the total profit from producing spare automobile parts while considering the available capacity in each shop.

Let's define the variables and parameters:

- Let \( x_k \) be the number of spare parts of type \( k \) to be produced.
- \( \text{profit}_k \) is the profit earned from producing one unit of part \( k \).
- \( \text{time}_{k,s} \) is the worker-hours required in shop \( s \) to produce one unit of part \( k \).
- \( \text{capacity}_s \) is the total available worker-hours in shop \( s \).

The objective is to maximize the total profit:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

Subject to the following constraints:

1. For each shop \( s \), the total worker-hours used does not exceed the available capacity:

\[
\sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s \quad \text{for } s = 1, 2, \ldots, S
\]

2. The number of parts produced cannot be negative:

\[
x_k \geq 0 \quad \text{for } k = 1, 2, \ldots, K
\]

Here's how the LP model can be written in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to:}

\begin{align*}
& \sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s, \quad \text{for } s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\end{align*}

\end{document}
```

This Linear Programming model will help determine the optimal number of each type of spare part to produce in order to maximize profits while respecting the shop capacity constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to:}

\begin{align*}
& \sum_{k=1}^{K} \text{time}_{k,s} \cdot x_k \leq \text{capacity}_s, \quad \text{for } s = 1, 2, \ldots, S \\
& x_k \geq 0, \quad \text{for } k = 1, 2, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Extracting values from the data
time = data['time']
profit = data['profit']
capacity = data['capacity']
K = len(profit)  #### Number of products
S = len(capacity)  #### Number of capacities

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Objective"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

