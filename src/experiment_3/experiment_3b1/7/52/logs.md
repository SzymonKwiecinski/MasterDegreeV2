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

\section*{Linear Programming Model for Electricity Distribution}

\textbf{Indices:}
\begin{itemize}
    \item $p$: index for power plants, where $p = 1, \ldots, P$
    \item $c$: index for cities, where $c = 1, \ldots, C$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $supply_p$: Capacity of power plant $p$ (in million kWh)
    \item $demand_c$: Peak demand of city $c$ (in million kWh)
    \item $transmission_{p,c}$: Transmission cost from power plant $p$ to city $c$ (in $/million kWh)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $send_{p,c}$: Amount of electricity sent from power plant $p$ to city $c$ (in million kWh)
\end{itemize}

\textbf{Objective:}
\[
\text{Minimize } Z = \sum_{p=1}^{P} \sum_{c=1}^{C} transmission_{p,c} \cdot send_{p,c}
\]

\textbf{Subject to:}
\begin{align*}
\sum_{c=1}^{C} send_{p,c} & \leq supply_p, & \forall p = 1, \ldots, P \quad \text{(Supply constraints)} \\
\sum_{p=1}^{P} send_{p,c} & \geq demand_c, & \forall c = 1, \ldots, C \quad \text{(Demand constraints)} \\
send_{p,c} & \geq 0, & \forall p, c \quad \text{(Non-negativity constraints)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $send_{p,c}$: Amount of electricity sent from power plant $p$ to city $c$ (in million kWh)
    \item $total\_cost$: Total transmission cost for the utility
\end{itemize}

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

\section*{Linear Programming Model for Electricity Distribution}

\textbf{Indices:}
\begin{itemize}
    \item $p$: index for power plants, where $p = 1, \ldots, P$
    \item $c$: index for cities, where $c = 1, \ldots, C$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $supply_p$: Capacity of power plant $p$ (in million kWh)
    \item $demand_c$: Peak demand of city $c$ (in million kWh)
    \item $transmission_{p,c}$: Transmission cost from power plant $p$ to city $c$ (in $/million kWh)
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $send_{p,c}$: Amount of electricity sent from power plant $p$ to city $c$ (in million kWh)
\end{itemize}

\textbf{Objective:}
\[
\text{Minimize } Z = \sum_{p=1}^{P} \sum_{c=1}^{C} transmission_{p,c} \cdot send_{p,c}
\]

\textbf{Subject to:}
\begin{align*}
\sum_{c=1}^{C} send_{p,c} & \leq supply_p, & \forall p = 1, \ldots, P \quad \text{(Supply constraints)} \\
\sum_{p=1}^{P} send_{p,c} & \geq demand_c, & \forall c = 1, \ldots, C \quad \text{(Demand constraints)} \\
send_{p,c} & \geq 0, & \forall p, c \quad \text{(Non-negativity constraints)}
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $send_{p,c}$: Amount of electricity sent from power plant $p$ to city $c$ (in million kWh)
    \item $total\_cost$: Total transmission cost for the utility
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data extraction from JSON format
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

#### Indices
P = len(data['supply'])  #### Number of power plants
C = len(data['demand'])   #### Number of cities

#### Initialize the problem
problem = pulp.LpProblem("ElectricityDistribution", pulp.LpMinimize)

#### Decision Variables: send_{p,c}
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

#### Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

#### Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

#### Solve the problem
problem.solve()

#### Output the results
for p in range(P):
    for c in range(C):
        print(f'Send from power plant {p+1} to city {c+1}: {send[p][c].varValue} million kWh')

total_cost = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

