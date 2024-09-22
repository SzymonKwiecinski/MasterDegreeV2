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
To formulate the problem of maximizing the firm's total revenue given the constraints on raw materials, we can create a linear programming model. Let's denote the variables as follows:

- Let \( x_j \) represent the amount of good \( j \) produced.

**Objective:**

Maximize the total revenue, which can be expressed as:

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

**Subject to:**

Each good requires a certain amount of raw materials, and the total usage of each raw material cannot exceed its available amount. These constraints can be expressed for each raw material \( i \) as:

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
\]

Additionally, we have non-negativity constraints for the production amounts:

\[
x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
\]

Here is the corresponding formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Objective:}

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\textbf{Subject to:}

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
\]

\[
x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
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

\section*{Linear Programming Formulation}

\textbf{Objective:}

\[
\text{Maximize} \quad Z = \sum_{j=1}^{M} \text{price}_j \cdot x_j
\]

\textbf{Subject to:}

\[
\sum_{j=1}^{M} \text{req}_{i,j} \cdot x_j \leq \text{available}_i \quad \text{for each } i = 1, \ldots, N
\]

\[
x_j \geq 0 \quad \text{for each } j = 1, \ldots, M
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25], 'Requirements': [[3, 2, 0, 0, 0], [0, 5, 2, 1, 0], [1, 0, 0, 5, 3], [0, 3, 1, 1, 5]], 'Prices': [7, 10, 5, 9]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {'M': 4, 'N': 5, 'Available': [10, 20, 15, 35, 25],
        'Requirements': [[3, 2, 0, 0, 0], 
                        [0, 5, 2, 1, 0], 
                        [1, 0, 0, 5, 3], 
                        [0, 3, 1, 1, 5]], 
        'Prices': [7, 10, 5, 9]}

M = data['M']
N = data['N']
available = data['Available']
requirements = data['Requirements']
prices = data['Prices']

#### Create the linear programming problem
problem = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)

#### Define decision variables
x = pulp.LpVariable.dicts("x", range(M), lowBound=0)

#### Objective function
problem += pulp.lpSum(prices[j] * x[j] for j in range(M)), "Objective"

#### Constraints
for i in range(N):
    problem += pulp.lpSum(requirements[j][i] * x[j] for j in range(M)) <= available[i], f"Constraint_{i+1}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

