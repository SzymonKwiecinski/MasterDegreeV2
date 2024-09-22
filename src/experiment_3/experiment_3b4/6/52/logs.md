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
To solve this problem, we will set up a linear programming model to minimize the total transmission cost while ensuring that all cities' demands are met without exceeding the supply capacity of each power plant.

Let:
- \( P \) be the number of power plants.
- \( C \) be the number of cities.
- \( \text{supply}_p \) be the supply capacity of power plant \( p \) in million kwh.
- \( \text{demand}_c \) be the demand of city \( c \) in million kwh.
- \( \text{transmission}_{p,c} \) be the transmission cost from power plant \( p \) to city \( c \) in dollars per million kwh.
- \( \text{send}_{p,c} \) be the decision variable representing the amount of electricity power plant \( p \) sends to city \( c \) in million kwh.

The objective is to minimize the total transmission cost:

\[
\text{Minimize } \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

Subject to the following constraints:
1. Each city's demand must be met:

\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_c \quad \forall c = 1, \ldots, C
\]

2. The amount sent from each power plant should not exceed its capacity:

\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraint:

\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
\]

Here is the linear programming model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Transmission}

\textbf{Objective:}

Minimize the total transmission cost
\[
\text{Minimize} \quad Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Subject to:}

1. Demand satisfaction for each city:
\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_c \quad \forall c = 1, \ldots, C
\]

2. Supply capacity constraint for each power plant:
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraint:
\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
\]

\end{document}
```

This model can be solved using linear programming techniques or solvers to determine the optimal values of \(\text{send}_{p,c}\) that minimize the total transmission cost \(Z\).

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Transmission}

\textbf{Objective:}

Minimize the total transmission cost
\[
\text{Minimize} \quad Z = \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\textbf{Subject to:}

1. Demand satisfaction for each city:
\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_c \quad \forall c = 1, \ldots, C
\]

2. Supply capacity constraint for each power plant:
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p \quad \forall p = 1, \ldots, P
\]

3. Non-negativity constraint:
\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
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

#### Parameters
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)
C = len(demand)

#### Problem
problem = pulp.LpProblem("Electricity_Transmission_Problem", pulp.LpMinimize)

#### Decision Variables
send = pulp.LpVariable.dicts("send",
                             ((p, c) for p in range(P) for c in range(C)),
                             lowBound=0,
                             cat='Continuous')

#### Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

#### Constraints
#### Demand satisfaction for each city
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_City_{c}"

#### Supply capacity constraint for each power plant
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_Plant_{p}"

#### Solve
problem.solve()

#### Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

