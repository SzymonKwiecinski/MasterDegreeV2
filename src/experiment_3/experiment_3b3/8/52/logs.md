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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Electricity Distribution}

\textbf{Indices:} \\
Let \( p \) denote the index for power plants, where \( p = 1, 2, \ldots, P \). \\
Let \( c \) denote the index for cities, where \( c = 1, 2, \ldots, C \).

\textbf{Parameters:} \\
Let \( supply_{p} \) be the capacity of power plant \( p \) (in million kWh). \\
Let \( demand_{c} \) be the peak demand of city \( c \) (in million kWh). \\
Let \( transmission_{p,c} \) be the transmission cost of power plant \( p \) supplying city \( c \) (in \$ per million kWh).

\textbf{Variables:} \\
Let \( send_{p,c} \) be the amount of electricity (in million kWh) that power plant \( p \) sends to city \( c \).

\textbf{Objective Function:} \\
Minimize the total transmission cost:
\[
\text{Minimize } Z = \sum_{p=1}^{P} \sum_{c=1}^{C} transmission_{p,c} \cdot send_{p,c}
\]

\textbf{Constraints:} \\
1. Demand constraints for each city:
\[
\sum_{p=1}^{P} send_{p,c} = demand_{c}, \quad \forall c = 1, 2, \ldots, C
\]
2. Supply constraints for each power plant:
\[
\sum_{c=1}^{C} send_{p,c} \leq supply_{p}, \quad \forall p = 1, 2, \ldots, P
\]
3. Non-negativity constraints:
\[
send_{p,c} \geq 0, \quad \forall p = 1, 2, \ldots, P, \quad \forall c = 1, 2, \ldots, C
\]

\textbf{Output Information:} \\
The solution will provide:
- \( send_{p,c} \): the amount of electricity power plant \( p \) sends to city \( c \) (in million kWh).
- \( total\_cost \): the total transmission cost for the utility.

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

\section*{Mathematical Model for Electricity Distribution}

\textbf{Indices:} \\
Let \( p \) denote the index for power plants, where \( p = 1, 2, \ldots, P \). \\
Let \( c \) denote the index for cities, where \( c = 1, 2, \ldots, C \).

\textbf{Parameters:} \\
Let \( supply_{p} \) be the capacity of power plant \( p \) (in million kWh). \\
Let \( demand_{c} \) be the peak demand of city \( c \) (in million kWh). \\
Let \( transmission_{p,c} \) be the transmission cost of power plant \( p \) supplying city \( c \) (in \$ per million kWh).

\textbf{Variables:} \\
Let \( send_{p,c} \) be the amount of electricity (in million kWh) that power plant \( p \) sends to city \( c \).

\textbf{Objective Function:} \\
Minimize the total transmission cost:
\[
\text{Minimize } Z = \sum_{p=1}^{P} \sum_{c=1}^{C} transmission_{p,c} \cdot send_{p,c}
\]

\textbf{Constraints:} \\
1. Demand constraints for each city:
\[
\sum_{p=1}^{P} send_{p,c} = demand_{c}, \quad \forall c = 1, 2, \ldots, C
\]
2. Supply constraints for each power plant:
\[
\sum_{c=1}^{C} send_{p,c} \leq supply_{p}, \quad \forall p = 1, 2, \ldots, P
\]
3. Non-negativity constraints:
\[
send_{p,c} \geq 0, \quad \forall p = 1, 2, \ldots, P, \quad \forall c = 1, 2, \ldots, C
\]

\textbf{Output Information:} \\
The solution will provide:
- \( send_{p,c} \): the amount of electricity power plant \( p \) sends to city \( c \) (in million kWh).
- \( total\_cost \): the total transmission cost for the utility.

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
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

#### Indices
P = len(supply)
C = len(demand)

#### Problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

#### Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

#### Constraints

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == demand[c], f"Demand_Constraint_City_{c}"

#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_Power_Plant_{p}"

#### Solve the problem
problem.solve()

#### Output results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for p in range(P):
    for c in range(C):
        print(f'Power Plant {p+1} sends {send[p,c].varValue} million kWh to City {c+1}')
```

