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
To address the problem of minimizing the total transmission cost of sending electricity from power plants to cities, we will define a Linear Programming (LP) model. The decision variables, constraints, and objective function will be clearly defined as follows.

######### Decision Variables:
- \( \text{send}_{p,c} \): Amount of electricity (in million kwh) sent from power plant \( p \) to city \( c \).

######### Objective Function:
- Minimize the total transmission cost:

\[
\text{Total Cost} = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

######### Constraints:
1. Supply Constraints: Each power plant cannot supply more electricity than its capacity.
   \[
   \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p} \quad \text{for each } p = 1, \ldots, P
   \]

2. Demand Constraints: Each city must receive its total electricity demand.
   \[
   \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c} \quad \text{for each } c = 1, \ldots, C
   \]

3. Non-negativity Constraints: The amount of electricity sent must be non-negative.
   \[
   \text{send}_{p,c} \geq 0 \quad \text{for all } p, c
   \]

Below is the Linear Programming formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total transmission cost

\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Subject to:}

1. \textbf{Supply Constraints:}
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall p = 1, \ldots, P
\]

2. \textbf{Demand Constraints:}
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall c = 1, \ldots, C
\]

3. \textbf{Non-negativity Constraints:}
\[
\text{send}_{p,c} \geq 0, \quad \forall p, c
\]

\end{document}
```

This Linear Programming model ensures that we minimize the transmission cost while meeting all the power supply and demand constraints effectively. Each decision variable \( \text{send}_{p,c} \) represents the optimal amount of power to be sent from a given power plant \( p \) to a city \( c \).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total transmission cost

\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Subject to:}

1. \textbf{Supply Constraints:}
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, \quad \forall p = 1, \ldots, P
\]

2. \textbf{Demand Constraints:}
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, \quad \forall c = 1, \ldots, C
\]

3. \textbf{Non-negativity Constraints:}
\[
\text{send}_{p,c} \geq 0, \quad \forall p, c
\]

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
supply = [30, 25, 45]
demand = [40, 60]
transmission_costs = [[14, 22], [18, 12], [10, 16]]

#### Indices
P = len(supply)
C = len(demand)

#### Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Decision Variables
send_vars = pulp.LpVariable.dicts(
    "send",
    ((p, c) for p in range(P) for c in range(C)),
    lowBound=0,
    cat='Continuous'
)

#### Objective
problem += pulp.lpSum(
    transmission_costs[p][c] * send_vars[(p, c)]
    for p in range(P)
    for c in range(C)
)

#### Supply Constraints
for p in range(P):
    problem += pulp.lpSum(
        send_vars[(p, c)] for c in range(C)
    ) <= supply[p], f"Supply_Constraint_{p}"

#### Demand Constraints
for c in range(C):
    problem += pulp.lpSum(
        send_vars[(p, c)] for p in range(P)
    ) == demand[c], f"Demand_Constraint_{c}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

