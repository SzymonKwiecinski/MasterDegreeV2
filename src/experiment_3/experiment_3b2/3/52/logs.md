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
The problem described is a classic transportation linear programming problem where the goal is to minimize the total transmission cost of supplying electricity from power plants to cities. The constraints involve ensuring supply limits from each plant and demand requirements for each city.

Below is the mathematical model represented in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model: Linear Programming for Electricity Distribution}

\subsection*{Sets and Indices}
- Let \( P \) be the set of power plants, indexed by \( p \).
- Let \( C \) be the set of cities, indexed by \( c \).

\subsection*{Parameters}
- \( \text{supply}_p \): the capacity of power plant \( p \) in million kWh.
- \( \text{demand}_c \): the peak demand of city \( c \) in million kWh.
- \( \text{transmission}_{p,c} \): the transmission cost from power plant \( p \) to city \( c \) in \$/million kWh.

\subsection*{Decision Variables}
- \( \text{send}_{p,c} \): the amount of electricity sent from power plant \( p \) to city \( c \) in million kWh.

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c} 
\]

\subsection*{Constraints}
1. Supply Constraints for each power plant:
   \[
   \sum_{c \in C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p \in P
   \]

2. Demand Constraints for each city:
   \[
   \sum_{p \in P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c \in C
   \]

3. Non-negativity Constraints:
   \[
   \text{send}_{p,c} \geq 0, \quad \forall p \in P, \forall c \in C
   \]

\subsection*{Output}
- The optimal \( \text{send}_{p,c} \) for all \( p \in P \) and \( c \in C \).
- The total transmission cost: \( \text{total\_cost} = \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c} \).

\end{document}
```

This LaTeX document provides a complete mathematical formulation of the problem, including the objective function, constraints, and decision variables. The solution to this linear programming problem will yield the optimal allocation of electricity from power plants to cities, minimizing the total transmission cost.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model: Linear Programming for Electricity Distribution}

\subsection*{Sets and Indices}
- Let \( P \) be the set of power plants, indexed by \( p \).
- Let \( C \) be the set of cities, indexed by \( c \).

\subsection*{Parameters}
- \( \text{supply}_p \): the capacity of power plant \( p \) in million kWh.
- \( \text{demand}_c \): the peak demand of city \( c \) in million kWh.
- \( \text{transmission}_{p,c} \): the transmission cost from power plant \( p \) to city \( c \) in \$/million kWh.

\subsection*{Decision Variables}
- \( \text{send}_{p,c} \): the amount of electricity sent from power plant \( p \) to city \( c \) in million kWh.

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{Minimize} \quad \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c} 
\]

\subsection*{Constraints}
1. Supply Constraints for each power plant:
   \[
   \sum_{c \in C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p \in P
   \]

2. Demand Constraints for each city:
   \[
   \sum_{p \in P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c \in C
   \]

3. Non-negativity Constraints:
   \[
   \text{send}_{p,c} \geq 0, \quad \forall p \in P, \forall c \in C
   \]

\subsection*{Output}
- The optimal \( \text{send}_{p,c} \) for all \( p \in P \) and \( c \in C \).
- The total transmission cost: \( \text{total\_cost} = \sum_{p \in P} \sum_{c \in C} \text{transmission}_{p,c} \times \text{send}_{p,c} \).

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"supply": [30, 25, 45], "demand": [40, 60], "transmission_costs": [[14, 22], [18, 12], [10, 16]]}')
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

#### Sets and Indices
P = range(len(supply))  #### Power plants indices
C = range(len(demand))   #### Cities indices

#### Problem Definition
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

#### Decision Variables
send = pulp.LpVariable.dicts("send", (P, C), lowBound=0)

#### Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in P for c in C)

#### Supply Constraints
for p in P:
    problem += pulp.lpSum(send[p][c] for c in C) <= supply[p]

#### Demand Constraints
for c in C:
    problem += pulp.lpSum(send[p][c] for p in P) == demand[c]

#### Solve the problem
problem.solve()

#### Output results
for p in P:
    for c in C:
        print(f'Send from Power Plant {p} to City {c}: {send[p][c].varValue} million kWh')

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

