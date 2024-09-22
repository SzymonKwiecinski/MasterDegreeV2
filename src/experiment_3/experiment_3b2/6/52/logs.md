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
To create a mathematical model for this problem, we will use Linear Programming (LP). The goal is to minimize the total transmission cost of sending electricity from power plants to cities while satisfying constraints related to supply and demand.

Let's define the decision variables, objective function, and constraints:

- Let \( \text{send}_{p,c} \) be the amount of electricity sent from power plant \( p \) to city \( c \).
- We want to minimize the total transmission cost: 
  \[
  \min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
  \]

######### Constraints:

1. **Supply Constraint**: Each power plant \( p \) cannot send more electricity than its capacity:
   \[
   \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p = 1, \ldots, P
   \]

2. **Demand Constraint**: Each city \( c \) must receive exactly its demand:
   \[
   \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c = 1, \ldots, C
   \]

3. **Non-negativity Constraint**: The amount of electricity sent must be non-negative:
   \[
   \text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
   \]

Here is the complete Linear Program written in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( \text{send}_{p,c} \) be the amount of electricity sent from power plant \( p \) to city \( c \).

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}

1. Supply constraints for each power plant \( p \):
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p = 1, \ldots, P
\]

2. Demand constraints for each city \( c \):
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c = 1, \ldots, C
\]

3. Non-negativity constraints:
\[
\text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
\]

\end{document}
```

This LaTeX code models the problem as a linear program. The constraints ensure that each power plant does not exceed its capacity, each city's demand is exactly met, and all shipments are non-negative. The objective function captures the goal of minimizing the total transmission cost.

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

\subsection*{Decision Variables}
Let \( \text{send}_{p,c} \) be the amount of electricity sent from power plant \( p \) to city \( c \).

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\min \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \times \text{send}_{p,c}
\]

\subsection*{Constraints}

1. Supply constraints for each power plant \( p \):
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_p, \quad \forall p = 1, \ldots, P
\]

2. Demand constraints for each city \( c \):
\[
\sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_c, \quad \forall c = 1, \ldots, C
\]

3. Non-negativity constraints:
\[
\text{send}_{p,c} \geq 0, \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
\]

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

#### Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

#### Create a linear programming problem
problem = pulp.LpProblem("Electricity_Transmission", pulp.LpMinimize)

#### Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

