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
To solve this problem, we need to formulate a linear programming model that minimizes the total transmission cost while meeting all supply and demand constraints. Let's define the variables, constraints, and the objective function for this linear program.

######### Variables
- Let \( \text{send}_{p,c} \) be the amount of electricity (in million kwh) sent from power plant \( p \) to city \( c \).

######### Objective Function
- Minimize the total transmission cost:
  \[
  \text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
  \]

######### Constraints
1. **Supply constraints**: Each power plant can only supply up to its capacity:
   \[
   \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p} \quad \forall p = 1, \ldots, P
   \]

2. **Demand constraints**: Each city's peak demand must be met:
   \[
   \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c} \quad \forall c = 1, \ldots, C
   \]

3. **Non-negativity constraints**: The amount of electricity sent must be non-negative:
   \[
   \text{send}_{p,c} \geq 0 \quad \forall p = 1, \ldots, P, \, c = 1, \ldots, C
   \]

Let's represent this model in LaTeX code.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item $\text{send}_{p,c}$: The amount of electricity sent from power plant $p$ to city $c$ (million kWh).
\end{itemize}

\textbf{Objective:} Minimize the total transmission cost.
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
\]

\textbf{Constraints:}
\begin{align*}
    & \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, & \forall p = 1, \ldots, P \quad &\text{(Supply constraints)} \\
    & \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, & \forall c = 1, \ldots, C \quad &\text{(Demand constraints)} \\
    & \text{send}_{p,c} \geq 0, & \forall p = 1, \ldots, P, \, c = 1, \ldots, C \quad &\text{(Non-negativity constraints)}
\end{align*}

\end{document}
```

This model will help determine the optimal amount of electricity each power plant should send to each city to minimize the total transmission cost while satisfying all supply and demand requirements.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item $\text{send}_{p,c}$: The amount of electricity sent from power plant $p$ to city $c$ (million kWh).
\end{itemize}

\textbf{Objective:} Minimize the total transmission cost.
\[
\text{Minimize} \quad \sum_{p=1}^{P} \sum_{c=1}^{C} \text{transmission}_{p,c} \cdot \text{send}_{p,c}
\]

\textbf{Constraints:}
\begin{align*}
    & \sum_{c=1}^{C} \text{send}_{p,c} \leq \text{supply}_{p}, & \forall p = 1, \ldots, P \quad &\text{(Supply constraints)} \\
    & \sum_{p=1}^{P} \text{send}_{p,c} = \text{demand}_{c}, & \forall c = 1, \ldots, C \quad &\text{(Demand constraints)} \\
    & \text{send}_{p,c} \geq 0, & \forall p = 1, \ldots, P, \, c = 1, \ldots, C \quad &\text{(Non-negativity constraints)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'supply': [30, 25, 45], 
        'demand': [40, 60], 
        'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

num_power_plants = len(supply)
num_cities = len(demand)

#### Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Variables
send = pulp.LpVariable.dicts("send", 
                             ((p, c) for p in range(num_power_plants) for c in range(num_cities)), 
                             lowBound=0, 
                             cat=pulp.LpContinuous)

#### Objective
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] 
                      for p in range(num_power_plants) 
                      for c in range(num_cities))

#### Supply constraints
for p in range(num_power_plants):
    problem += pulp.lpSum(send[p, c] for c in range(num_cities)) <= supply[p]

#### Demand constraints
for c in range(num_cities):
    problem += pulp.lpSum(send[p, c] for p in range(num_power_plants)) == demand[c]

#### Solve
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

