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
To formulate this problem as a linear programming model, we need to define the decision variables, objective function, and constraints based on the given information.

######### Decision Variables
Let \( x_l \) be the number of times process \( l \) is executed for \( l = 1, \ldots, L \).

######### Objective Function
The objective is to maximize the total revenue, which is the total sales revenue from the products minus the cost of executing the processes. Mathematically, this can be expressed as:

\[
\text{Maximize:} \quad \sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l \right) \cdot \text{price}_p - \sum_{l=1}^{L} \text{cost}_l \cdot x_l
\]

######### Constraints
1. **Crude Oil Allocation Constraint**: For each type of crude oil \( i \), the total input used by all processes must not exceed the allocated amount:

\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \text{for all } i = 1, \ldots, O
\]

2. **Non-Negativity Constraints**: The number of executions of each process must be non-negative:

\[
x_l \geq 0 \quad \text{for all } l = 1, \ldots, L
\]

Let us formulate this in a LaTeX document.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Maximize:}
\[
\sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l \right) \cdot \text{price}_p - \sum_{l=1}^{L} \text{cost}_l \cdot x_l
\]

\textbf{Subject to:}
\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \text{for all } i = 1, \ldots, O
\]

\[
x_l \geq 0 \quad \text{for all } l = 1, \ldots, L
\]

\end{document}
```

This LaTeX document describes the linear programming model required to determine the optimal number of times each process should be executed to maximize revenue, given the constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Maximize:}
\[
\sum_{p=1}^{P} \left( \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l \right) \cdot \text{price}_p - \sum_{l=1}^{L} \text{cost}_l \cdot x_l
\]

\textbf{Subject to:}
\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i \quad \text{for all } i = 1, \ldots, O
\]

\[
x_l \geq 0 \quad \text{for all } l = 1, \ldots, L
\]

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Define variables
x = pulp.LpVariable.dicts("x", range(data['L']), lowBound=0)

#### Define the objective function
profit = pulp.lpSum([(pulp.lpSum([data['Output'][l][p] * x[l] for l in range(data['L'])]) * data['Price'][p]) for p in range(data['P'])]) - pulp.lpSum([data['Cost'][l] * x[l] for l in range(data['L'])])
problem += profit

#### Constraints
for i in range(data['O']):
    problem += pulp.lpSum([data['Input'][l][i] * x[l] for l in range(data['L'])]) <= data['Allocated'][i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

