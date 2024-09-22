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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Oil Refinery Production}

\subsection*{Parameters}
\begin{align*}
\text{Let } O & \text{ be the number of crude oil types.} \\
\text{Let } P & \text{ be the number of products.} \\
\text{Let } L & \text{ be the number of production processes.} \\
\text{Let } \text{allocated}_i & \text{ be the quantity of crude oil type } i \text{ (in million barrels).} \\
\text{Let } \text{price}_p & \text{ be the selling price of product } p \text{ (in dollars per barrel).} \\
\text{Let } \text{input}_{l,i} & \text{ be the quantity of crude oil type } i \text{ needed for process } l. \\
\text{Let } \text{output}_{l,p} & \text{ be the quantity of product } p \text{ produced by process } l. \\
\text{Let } \text{cost}_l & \text{ be the cost per barrel for process } l.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{Let } x_l & \text{ be the number of times process } l \text{ is executed.}
\end{align*}

\subsection*{Objective Function}
Maximize total revenue:
\[
\text{revenue} = \sum_{p=1}^{P} \text{price}_p \cdot \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l
\]

\subsection*{Constraints}
1. Crude oil availability:
\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i, \quad \forall i \in \{1, \ldots, O\}
\]

2. Non-negativity:
\[
x_l \geq 0, \quad \forall l \in \{1, \ldots, L\}
\]

\subsection*{Output}
The output of the model will provide:
\begin{align*}
\text{revenue} & \text{ is the total revenue for the month.} \\
\text{execute}_l & \text{ is the number of times that process } l \text{ should be executed.}
\end{align*}

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

\section*{Linear Programming Model for Oil Refinery Production}

\subsection*{Parameters}
\begin{align*}
\text{Let } O & \text{ be the number of crude oil types.} \\
\text{Let } P & \text{ be the number of products.} \\
\text{Let } L & \text{ be the number of production processes.} \\
\text{Let } \text{allocated}_i & \text{ be the quantity of crude oil type } i \text{ (in million barrels).} \\
\text{Let } \text{price}_p & \text{ be the selling price of product } p \text{ (in dollars per barrel).} \\
\text{Let } \text{input}_{l,i} & \text{ be the quantity of crude oil type } i \text{ needed for process } l. \\
\text{Let } \text{output}_{l,p} & \text{ be the quantity of product } p \text{ produced by process } l. \\
\text{Let } \text{cost}_l & \text{ be the cost per barrel for process } l.
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{Let } x_l & \text{ be the number of times process } l \text{ is executed.}
\end{align*}

\subsection*{Objective Function}
Maximize total revenue:
\[
\text{revenue} = \sum_{p=1}^{P} \text{price}_p \cdot \sum_{l=1}^{L} \text{output}_{l,p} \cdot x_l
\]

\subsection*{Constraints}
1. Crude oil availability:
\[
\sum_{l=1}^{L} \text{input}_{l,i} \cdot x_l \leq \text{allocated}_i, \quad \forall i \in \{1, \ldots, O\}
\]

2. Non-negativity:
\[
x_l \geq 0, \quad \forall l \in \{1, \ldots, L\}
\]

\subsection*{Output}
The output of the model will provide:
\begin{align*}
\text{revenue} & \text{ is the total revenue for the month.} \\
\text{execute}_l & \text{ is the number of times that process } l \text{ should be executed.}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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

#### Parameters
O = data['O']
P = data['P']
L = data['L']
Allocated = data['Allocated']
Price = data['Price']
Input = data['Input']
Output = data['Output']
Cost = data['Cost']

#### Create a linear programming problem
problem = pulp.LpProblem("OilRefineryProduction", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("ProcessExecution", range(L), lowBound=0)

#### Objective Function
problem += pulp.lpSum(Price[p] * pulp.lpSum(Output[l][p] * x[l] for l in range(L)) for p in range(P)), "TotalRevenue"

#### Constraints
for i in range(O):
    problem += pulp.lpSum(Input[l][i] * x[l] for l in range(L)) <= Allocated[i], f"CrudeOilAvailability_{i}"

#### Solve the problem
problem.solve()

#### Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Print number of times each process should be executed
for l in range(L):
    print(f'Process {l}: {pulp.value(x[l])}')
```

