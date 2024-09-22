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
To address the given problem, we will create a linear programming model to maximize the revenue by determining how many times each process should be executed.

######### Model Variables:
- Let \( x_l \) be the number of times process \( l \) is executed for \( l = 1, \ldots, L \).

######### Objective Function:
Maximize the total revenue, which is formulated as:

\[
\text{Revenue} = \sum_{p=1}^{P} \left( \text{price}_p \sum_{l=1}^{L} \text{output}_{l,p} x_l \right) - \sum_{l=1}^{L} \text{cost}_l \sum_{p=1}^{P} \text{output}_{l,p} x_l
\]

Simplified, the objective function becomes:

\[
\max \sum_{p=1}^{P} \sum_{l=1}^{L} \left( \text{price}_p \cdot \text{output}_{l,p} - \text{cost}_l \cdot \text{output}_{l,p} \right) x_l
\]

######### Constraints:
1. Crude oil supply constraints: For each crude oil type \( i \):

\[
\sum_{l=1}^{L} \text{input}_{l,i} x_l \leq \text{allocated}_i \quad \text{for } i = 1, \ldots, O
\]

2. Non-negativity constraints: 

\[
x_l \geq 0 \quad \text{for } l = 1, \ldots, L
\]

######### Formulation in LaTeX:
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Maximize Revenue}

\subsection*{Decision Variables}
Let \( x_l \) be the number of times process \( l \) is executed, \( l = 1, \ldots, L \).

\subsection*{Objective Function}
Maximize:
\[
\sum_{p=1}^{P} \sum_{l=1}^{L} \left( \text{price}_p \cdot \text{output}_{l,p} - \text{cost}_l \cdot \text{output}_{l,p} \right) x_l
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Crude oil supply constraints:} For each crude oil type \( i \):
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} x_l \leq \text{allocated}_i \quad \text{for } i = 1, \ldots, O
    \]

    \item \textbf{Non-negativity:}
    \[
    x_l \geq 0 \quad \text{for } l = 1, \ldots, L
    \]
\end{enumerate}

\end{document}
```

This formulation ensures that the optimal execution levels for each process are determined such that the revenue for the refinery is maximized while respecting the available crude oil allocations.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model to Maximize Revenue}

\subsection*{Decision Variables}
Let \( x_l \) be the number of times process \( l \) is executed, \( l = 1, \ldots, L \).

\subsection*{Objective Function}
Maximize:
\[
\sum_{p=1}^{P} \sum_{l=1}^{L} \left( \text{price}_p \cdot \text{output}_{l,p} - \text{cost}_l \cdot \text{output}_{l,p} \right) x_l
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Crude oil supply constraints:} For each crude oil type \( i \):
    \[
    \sum_{l=1}^{L} \text{input}_{l,i} x_l \leq \text{allocated}_i \quad \text{for } i = 1, \ldots, O
    \]

    \item \textbf{Non-negativity:}
    \[
    x_l \geq 0 \quad \text{for } l = 1, \ldots, L
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

#### Create a linear programming problem (maximize revenue)
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(data['L'])]

#### Objective Function
objective = pulp.lpSum(
    (data['Price'][p] * data['Output'][l][p] - data['Cost'][l] * data['Output'][l][p]) * x[l]
    for p in range(data['P'])
    for l in range(data['L'])
)
problem += objective

#### Constraints
#### Crude oil supply constraints
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

