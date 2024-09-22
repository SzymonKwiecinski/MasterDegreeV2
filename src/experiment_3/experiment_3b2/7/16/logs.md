# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A manager of an oil refinery has \var{allocated_i} million barrels of crude oil type \var{i} allocated for production during the coming month. 
- These resources can be used to make \var{P} different products. product \var{p} sells for $ \var{price_p} per barrel.
- There are \var{L} production processes. Process \var{l} uses \var{input_l_i} barrels of each crude \var{i}, and produces \var{output_l_p} barrels of each product \var{p}. 
- Process \var{l} has a cost of \var{cost_l} per barrel of product produced.
- All \var{input_l_i} quantities and \var{output_l_p} quanitites are in barrels. 
- There are no separate cost items for the cost of the crudes, as they have already been allocated.

INPUT FORMAT: 

{
    "allocated": [allocated_i for i in 1, ..., O],
    "price": [price_p for p in 1, ..., P],
    "input": [[input_l_i for i in 1, ..., O] for l in 1, ..., L],
    "output": [[output_l_p for p in 1, ..., P] for l in 1, ..., L],
    "cost": [cost_l for l in 1, ..., L]
}

OBJECTIVE: We want to know how many times should we execute each process to maximize the revenue for the next month (you can assume that the number of times that each process is executed is a floating point number)

OUTPUT INFO:

- \var{revenue} is the total revenue for the month.
- \var{execute_l} is the number of times that process \var{l} should be executed.

OUTPUT FORMAT:

{
    "revenue": revenue,
    "execute": [execute_l for l in 1, ..., L]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve this problem, we need to formulate a Linear Programming (LP) model. Our objective is to maximize the revenue generated from producing products using the assigned crude oil resources through multiple production processes. Let's define the problem mathematically.

######### Variables

- Let \( x_l \) be the number of times process \( l \) is executed, where \( l = 1, \ldots, L \).

######### Objective Function

The objective is to maximize the total revenue minus the production cost:

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{price}_p \cdot x_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot x_l 
\]

######### Constraints

1. **Crude Oil Usage Constraints**: The total crude oil of type \( i \) used by all processes must not exceed the allocated amount:
\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \forall \, i = 1, \ldots, O
\]

2. **Non-negativity Constraints**: The number of times each process is executed must be non-negative:
\[
x_l \geq 0 \quad \forall \, l = 1, \ldots, L
\]

Here is the corresponding formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Oil Refinery Problem}

\noindent \textbf{Decision Variables:}
\begin{itemize}
    \item \( x_l \) = Number of times process \( l \) is executed, \( l = 1, \ldots, L \).
\end{itemize}

\noindent \textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{price}_p \cdot x_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot x_l 
\]

\noindent \textbf{Subject to:}

\begin{align*}
    & \sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \forall \, i = 1, \ldots, O \\
    & x_l \geq 0 \quad \forall \, l = 1, \ldots, L
\end{align*}

\end{document}
```

This model aims to determine the optimal number of executions for each process that maximizes the revenue while respecting the constraints on crude oil allocation.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Oil Refinery Problem}

\noindent \textbf{Decision Variables:}
\begin{itemize}
    \item \( x_l \) = Number of times process \( l \) is executed, \( l = 1, \ldots, L \).
\end{itemize}

\noindent \textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{price}_p \cdot x_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot x_l 
\]

\noindent \textbf{Subject to:}

\begin{align*}
    & \sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \forall \, i = 1, \ldots, O \\
    & x_l \geq 0 \quad \forall \, l = 1, \ldots, L
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000], 
    'Price': [38, 33], 
    'Input': [[3, 5], [1, 1], [5, 3]], 
    'Output': [[4, 3], [1, 1], [3, 4]], 
    'Cost': [51, 11, 40]
}

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

#### Create the problem
problem = pulp.LpProblem("OilRefineryProblem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum([pulp.lpSum([output_data[l-1][p-1] * price[p-1] * x[l] for l in range(1, L + 1)]) for p in range(1, P + 1)]) - pulp.lpSum([cost[l-1] * x[l] for l in range(1, L + 1)])

#### Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum([input_data[l-1][i-1] * x[l] for l in range(1, L + 1)]) <= allocated[i-1]

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

