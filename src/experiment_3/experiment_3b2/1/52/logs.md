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
To model this problem as a linear programming problem, we define the following decision variables and constraints:

**Decision Variables:**
- Let \( x_{p,c} \) be the amount of electricity (in million kwh) that power plant \( p \) sends to city \( c \).

**Objective Function:**
- Minimize the total transmission cost, which is given by:
  
  \[
  \text{minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot x_{p,c}
  \]

**Constraints:**
1. **Supply Constraints for Power Plants:**
   Each power plant \( p \) cannot supply more than its capacity:
   \[
   \sum_{c=1}^{C} x_{p,c} \leq \text{supply}_{p}, \quad \forall p \in \{1, \ldots, P\}
   \]

2. **Demand Constraints for Cities:**
   The demand of each city \( c \) must be fully met:
   \[
   \sum_{p=1}^{P} x_{p,c} \geq \text{demand}_{c}, \quad \forall c \in \{1, \ldots, C\}
   \]

3. **Non-negativity Constraints:**
   \[
   x_{p,c} \geq 0, \quad \forall p \in \{1, \ldots, P\}, \ \forall c \in \{1, \ldots, C\}
   \]

Now we will present the linear programming formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let \( x_{p,c} \) be the amount of electricity that power plant \( p \) sends to city \( c \).

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot x_{p,c}
\]

\subsection*{Constraints}
1. Supply Constraints for Power Plants:
   \[
   \sum_{c=1}^{C} x_{p,c} \leq \text{supply}_{p}, \quad \forall p \in \{1, \ldots, P\}
   \]

2. Demand Constraints for Cities:
   \[
   \sum_{p=1}^{P} x_{p,c} \geq \text{demand}_{c}, \quad \forall c \in \{1, \ldots, C\}
   \]

3. Non-negativity Constraints:
   \[
   x_{p,c} \geq 0, \quad \forall p \in \{1, \ldots, P\}, \ \forall c \in \{1, \ldots, C\}
   \]

\end{document}
```

This formulation can be solved using a linear programming solver, and the output will provide the optimal values for \( x_{p,c} \), indicating how much electricity each power plant should send to each city to minimize the transmission cost. The solver will also provide the total transmission cost as the optimal objective value.

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
Let \( x_{p,c} \) be the amount of electricity that power plant \( p \) sends to city \( c \).

\subsection*{Objective Function}
Minimize the total transmission cost:
\[
\text{minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot x_{p,c}
\]

\subsection*{Constraints}
1. Supply Constraints for Power Plants:
   \[
   \sum_{c=1}^{C} x_{p,c} \leq \text{supply}_{p}, \quad \forall p \in \{1, \ldots, P\}
   \]

2. Demand Constraints for Cities:
   \[
   \sum_{p=1}^{P} x_{p,c} \geq \text{demand}_{c}, \quad \forall c \in \{1, \ldots, C\}
   \]

3. Non-negativity Constraints:
   \[
   x_{p,c} \geq 0, \quad \forall p \in \{1, \ldots, P\}, \ \forall c \in \{1, \ldots, C\}
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

#### Define the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Define decision variables
P = len(data['supply'])
C = len(data['demand'])
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C))

#### Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

#### Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

