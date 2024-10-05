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
To model this problem using linear programming, we need to define decision variables, an objective function, and constraints.

######### Decision Variables
Let \( \text{send}_{p,c} \) be the amount of electricity (in million kwh) that power plant \( p \) sends to city \( c \).

######### Objective Function
We aim to minimize the total transmission cost, which can be expressed as:

\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
\]

######### Constraints

1. **Supply Constraints:** Each power plant cannot supply more electricity than its capacity:

\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p} \quad \forall p = 1, \ldots, P
\]

2. **Demand Constraints:** Each city’s demand must be met:

\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_{c} \quad \forall c = 1, \ldots, C
\]

3. **Non-negativity Constraints:** Electricity sent should be non-negative:

\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \forall c = 1, \ldots, C
\]

######### LATEX Model

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
\]

\textbf{Subject to:}

\text{Supply Constraints:}
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p} \quad \forall p = 1, \ldots, P
\]

\text{Demand Constraints:}
\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_{c} \quad \forall c = 1, \ldots, C
\]

\text{Non-negativity Constraints:}
\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \forall c = 1, \ldots, C
\]

\end{document}
```

This setup will allow you to solve the linear programming problem to find the optimal distribution of electricity from the power plants to the cities, minimizing transmission costs while meeting all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
\]

\textbf{Subject to:}

\text{Supply Constraints:}
\[
\sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p} \quad \forall p = 1, \ldots, P
\]

\text{Demand Constraints:}
\[
\sum_{p=1}^{P} \text{send}_{p,c} \geq \text{demand}_{c} \quad \forall c = 1, \ldots, C
\]

\text{Non-negativity Constraints:}
\[
\text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \forall c = 1, \ldots, C
\]

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

#### Parameters
P = len(data['supply'])  #### Number of suppliers
C = len(data['demand'])   #### Number of consumers

#### Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Costs", pulp.LpMinimize)

#### Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

