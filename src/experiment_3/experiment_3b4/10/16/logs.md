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
To model the given problem as a Linear Programming (LP) problem, we'll need to set up decision variables, an objective function to maximize, and constraints based on the inputs provided.

Let's denote the decision variable for how many times process \( l \) is executed as \( x_l \).

**Objective Function:**

We aim to maximize the total revenue, which is computed by taking into account the revenue from selling products and the cost of the production processes. The objective function can be stated as:

\[ 
\text{Maximize } \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output\_l\_p} \times x_l \right) \times \text{price\_p} - \sum_{l=1}^{L} \text{cost\_l} \times \left( \sum_{p=1}^{P} \text{output\_l\_p} \times x_l \right)
\]

**Constraints:**

1. For each crude oil type \( i \), the total usage must not exceed the allocated barrels:

\[
\sum_{l=1}^{L} \text{input\_l\_i} \times x_l \leq \text{allocated\_i} \quad \text{for each crude oil } i
\]

2. Non-negativity constraint:

\[
x_l \geq 0 \quad \text{for each process } l
\]

Using the above formulation, the Linear Programming model can be implemented in LaTeX as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}

Let \( x_l \) be the number of times process \( l \) is executed.

\textbf{Objective Function:}

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output\_l\_p} \times x_l \right) \times \text{price\_p} - \sum_{l=1}^{L} \text{cost\_l} \times \left( \sum_{p=1}^{P} \text{output\_l\_p} \times x_l \right)
\]

\textbf{Subject to constraints:}

1. Resource allocation constraints for crude oils:

\[
\sum_{l=1}^{L} \text{input\_l\_i} \times x_l \leq \text{allocated\_i} \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraints:

\[
x_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\end{document}
``` 

This formulation captures the essence of the problem, balancing the production of saleable products using various processes with the constraints of available crude oil resources, while aiming to maximize the revenue.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Decision Variables:}

Let \( x_l \) be the number of times process \( l \) is executed.

\textbf{Objective Function:}

\[
\text{Maximize } Z = \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output\_l\_p} \times x_l \right) \times \text{price\_p} - \sum_{l=1}^{L} \text{cost\_l} \times \left( \sum_{p=1}^{P} \text{output\_l\_p} \times x_l \right)
\]

\textbf{Subject to constraints:}

1. Resource allocation constraints for crude oils:

\[
\sum_{l=1}^{L} \text{input\_l\_i} \times x_l \leq \text{allocated\_i} \quad \forall i = 1, \ldots, O
\]

2. Non-negativity constraints:

\[
x_l \geq 0 \quad \forall l = 1, \ldots, L
\]

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extracted from JSON
data = {
    'O': 2, 
    'P': 2, 
    'L': 3, 
    'Allocated': [8000, 5000],
    'Price': [38, 33], 
    'Input': [
        [3, 5],   #### Inputs for process 1
        [1, 1],   #### Inputs for process 2
        [5, 3]    #### Inputs for process 3
    ], 
    'Output': [
        [4, 3],   #### Outputs for process 1
        [1, 1],   #### Outputs for process 2
        [3, 4]    #### Outputs for process 3
    ], 
    'Cost': [51, 11, 40]
}

#### Number of resource types, products, and processes
O = data['O']
P = data['P']
L = data['L']

#### Extracting specific data
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(L)]

#### Objective function
objective = pulp.lpSum([
    pulp.lpSum([
        output_matrix[l][p] * x[l] for l in range(L)
    ]) * price[p] for p in range(P)
]) - pulp.lpSum([
    cost[l] * pulp.lpSum([
        output_matrix[l][p] * x[l] for p in range(P)
    ]) for l in range(L)
])

problem += objective

#### Constraints
for i in range(O):
    constraint = pulp.lpSum([
        input_matrix[l][i] * x[l] for l in range(L)
    ]) <= allocated[i]
    problem += constraint

#### Solve the problem
problem.solve()

#### Output the results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

