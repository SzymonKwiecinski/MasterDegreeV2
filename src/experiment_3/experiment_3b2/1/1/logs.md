# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A firm produces \var{M} different goods using \var{N} different raw materials.
- The firm has \var{available_{i}} of raw material \var{i} available.
- Good \var{j} requires \var{req_{i,j}} units of material \var{i} per unit produced.
- Good \var{j} results in a revenue of \var{price_j} per unit produced.


INPUT FORMAT: 

{
    "available": [available_{i} for i in 1, ..., N]
    "requirements": [[req_{i,j} for i in 1, ..., N] for j in 1, ..., M],
    "prices": [price_{j} for j in 1, ..., M]
}

OBJECTIVE: How much of each good should the firm produce in order to maximize its total revenue?

OUTPUT INFO:

- the amount of each good produced \var{amount_{j}}.

OUTPUT FORMAT:

{
    "amount": [amount_{j} for j in 1, ..., M]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model the given Linear Programming problem, we need to create an objective function and constraints that reflect the firm's production process. The goal is to maximize total revenue by determining the optimal production levels for each good, subject to the raw material constraints. Below is the mathematical formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Objective}
Maximize the total revenue, given by:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot \text{amount}_j
\]

\subsection*{Constraints}
Subject to the constraints on raw materials:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall \, i = 1, \ldots, N
\]

\subsection*{Non-negativity}
The production amounts cannot be negative:

\[
\text{amount}_j \geq 0, \quad \forall \, j = 1, \ldots, M
\]

\end{document}
```

In this model:
- The objective function `Z` represents the total revenue, which is to be maximized.
- Each constraint ensures that the usage of each raw material does not exceed its available quantity.
- The non-negativity constraints ensure that the amounts produced are zero or positive. 

This model can be solved using linear programming solvers to find the optimal production amounts for each good. 

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

\subsection*{Objective}
Maximize the total revenue, given by:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot \text{amount}_j
\]

\subsection*{Constraints}
Subject to the constraints on raw materials:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot \text{amount}_j \leq \text{available}_i, \quad \forall \, i = 1, \ldots, N
\]

\subsection*{Non-negativity}
The production amounts cannot be negative:

\[
\text{amount}_j \geq 0, \quad \forall \, j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data_json = '{"M": 4, "N": 5, "Available": [10, 20, 15, 35, 25], "Requirements": [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], "Prices": [7, 10, 5, 9]}'
data = json.loads(data_json)

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

#### Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define decision variables
amounts = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

#### Objective function
problem += pulp.lpSum(prices[j] * amounts[j] for j in range(M))

#### Constraints
for i in range(N):
    problem += (pulp.lpSum(requirements[j][i] * amounts[j] for j in range(M)) <= available[i])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

