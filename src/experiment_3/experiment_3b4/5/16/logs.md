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
To solve this problem using Linear Programming, we will define a mathematical formulation with an objective to maximize the total revenue. The decision variables will represent the number of times each production process is executed. Below is the mathematical formulation of the problem in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{align*}
O & : \text{Number of crude oil types} \\
P & : \text{Number of product types} \\
L & : \text{Number of production processes} \\
\text{allocated}_i & : \text{Barrels of crude oil type } i \text{ allocated} \quad (i = 1, \ldots, O) \\
\text{price}_p & : \text{Selling price per barrel of product } p \quad (p = 1, \ldots, P) \\
\text{input}_{l,i} & : \text{Barrels of crude type } i \text{ used in process } l \quad (l = 1, \ldots, L) \\
\text{output}_{l,p} & : \text{Barrels of product } p \text{ produced by process } l \quad (l = 1, \ldots, L) \\
\text{cost}_l & : \text{Cost per barrel of product produced by process } l \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{execute}_l & : \text{Number of times process } l \text{ is executed} \quad (l = 1, \ldots, L)
\end{align*}

\subsection*{Objective Function}

Maximize the total revenue:
\[
\text{revenue} = \sum_{p=1}^{P} \left( \text{price}_p \cdot \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{execute}_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot \sum_{p=1}^{P} \text{output}_{l,p} \cdot \text{execute}_l
\]

\subsection*{Constraints}

1. \textit{Crude Oil Availability:}
   For each crude oil type \( i \):
   \[
   \sum_{l=1}^{L} \text{input}_{l,i} \cdot \text{execute}_l \leq \text{allocated}_i
   \]

2. \textit{Non-negativity:}
   \[
   \text{execute}_l \geq 0 \quad \forall l = 1, \ldots, L
   \]

\end{document}
```

This mathematical formulation captures the constraints and objective for maximizing the refinery's revenue by determining the optimal number of times each process should execute given the constraints on crude oil availability and process costs.

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

\subsection*{Parameters}
\begin{align*}
O & : \text{Number of crude oil types} \\
P & : \text{Number of product types} \\
L & : \text{Number of production processes} \\
\text{allocated}_i & : \text{Barrels of crude oil type } i \text{ allocated} \quad (i = 1, \ldots, O) \\
\text{price}_p & : \text{Selling price per barrel of product } p \quad (p = 1, \ldots, P) \\
\text{input}_{l,i} & : \text{Barrels of crude type } i \text{ used in process } l \quad (l = 1, \ldots, L) \\
\text{output}_{l,p} & : \text{Barrels of product } p \text{ produced by process } l \quad (l = 1, \ldots, L) \\
\text{cost}_l & : \text{Cost per barrel of product produced by process } l \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{execute}_l & : \text{Number of times process } l \text{ is executed} \quad (l = 1, \ldots, L)
\end{align*}

\subsection*{Objective Function}

Maximize the total revenue:
\[
\text{revenue} = \sum_{p=1}^{P} \left( \text{price}_p \cdot \sum_{l=1}^{L} \text{output}_{l,p} \cdot \text{execute}_l \right) - \sum_{l=1}^{L} \text{cost}_l \cdot \sum_{p=1}^{P} \text{output}_{l,p} \cdot \text{execute}_l
\]

\subsection*{Constraints}

1. \textit{Crude Oil Availability:}
   For each crude oil type \( i \):
   \[
   \sum_{l=1}^{L} \text{input}_{l,i} \cdot \text{execute}_l \leq \text{allocated}_i
   \]

2. \textit{Non-negativity:}
   \[
   \text{execute}_l \geq 0 \quad \forall l = 1, \ldots, L
   \]

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

O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

#### Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

#### Decision Variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0, cat='Continuous')

#### Objective Function
revenue = pulp.lpSum(
    [price[p] * 
     pulp.lpSum([output_matrix[l][p] * execute[l] for l in range(L)]) 
     for p in range(P)]
) - pulp.lpSum(
    [cost[l] * 
     pulp.lpSum([output_matrix[l][p] * execute[l] for p in range(P)]) 
     for l in range(L)]
)

problem += revenue

#### Constraints
#### Crude Oil Availability
for i in range(O):
    problem += (pulp.lpSum([input_matrix[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Crude_Oil_Availability_{i}")

#### Solve Problem
problem.solve()

#### Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

