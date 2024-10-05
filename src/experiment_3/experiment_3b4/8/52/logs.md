# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A small electric utility operates \var{P} power plants to supply electricity to \var{C} cities.
- Each power plant has a capacity of \var{supply_{p}} million kwh.
- Each city has a peak demand of \var{demand_{c}} million kwh, which must be met at the same time.
- Power plant \var{p} can send electricity to city \var{c} at a transmission cost of \var{transmission_{p,c}} $/million kwh.

INPUT FORMAT: 

{
    "supply": [supply_{p} for p in 1, ..., P],
    "demand": [demand_{c} for c in 1, ..., C],
    "transmission_costs": [[transmission_{p,c} for c in 1, ..., C] for p in 1, ..., P]
}

OBJECTIVE: How much electricity should each power plant send to each city to minimize the total transmission cost?

OUTPUT INFO:

- the amount of electricity power plant \var{p} sends to city \var{c} as \var{send_{p,c}} million kwh.
- \var{total_cost} displays the total transmission cost for the utility.

OUTPUT FORMAT:

{
    "send": [[send_{p,c} for c in 1, ..., C] for p in 1, ..., P],
    "total_cost": total_cost
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this linear programming problem, we need to minimize the total transmission cost while satisfying the constraints of supply and demand. Let \( \text{send}_{p,c} \) be the amount of electricity sent from power plant \( p \) to city \( c \).

Here's the mathematical model for this problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}

Let \( \text{send}_{p,c} \) be the amount of electricity (in million kwh) sent from power plant \( p \) to city \( c \).

\textbf{Objective Function:}

Minimize the total transmission cost:
\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Constraints:}

1. Supply constraints for each power plant \( p \):
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall \, p = 1, \ldots, P
\]

2. Demand constraints for each city \( c \):
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall \, c = 1, \ldots, C
\]

3. Non-negativity constraints:
\[
\text{send}_{p,c} \geq 0, \quad \forall \, p = 1, \ldots, P, \, \forall \, c = 1, \ldots, C
\]

\end{document}
```

This LaTeX code provides a complete mathematical model for the linear programming problem. It includes decision variables, the objective function to be minimized, and the necessary constraints that ensure supply and demand are met while keeping all variables non-negative.

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

\textbf{Decision Variables:}

Let \( \text{send}_{p,c} \) be the amount of electricity (in million kwh) sent from power plant \( p \) to city \( c \).

\textbf{Objective Function:}

Minimize the total transmission cost:
\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Constraints:}

1. Supply constraints for each power plant \( p \):
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall \, p = 1, \ldots, P
\]

2. Demand constraints for each city \( c \):
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall \, c = 1, \ldots, C
\]

3. Non-negativity constraints:
\[
\text{send}_{p,c} \geq 0, \quad \forall \, p = 1, \ldots, P, \, \forall \, c = 1, \ldots, C
\]

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

num_plants = len(supply)
num_cities = len(demand)

#### Problem
problem = pulp.LpProblem("Minimize_Transmission_Costs", pulp.LpMinimize)

#### Decision Variables
send = pulp.LpVariable.dicts("Send", ((p, c) for p in range(num_plants) for c in range(num_cities)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(num_plants) for c in range(num_cities))

#### Supply Constraints
for p in range(num_plants):
    problem += pulp.lpSum(send[p, c] for c in range(num_cities)) <= supply[p]

#### Demand Constraints
for c in range(num_cities):
    problem += pulp.lpSum(send[p, c] for p in range(num_plants)) == demand[c]

#### Solve
problem.solve()

#### Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

