# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A seaport unloads shipping containers off of rail cars, holds them in its yard on a transport system, and then loads them onto ships.
- The demand \var{demand_{t}} for containers by ships varies every month, and this demand must be fulfilled.
- The unloading cost \var{unload_cost_{t}} per container indicates how much it costs to unload a single container from the rail car.
- The unloading capacity \var{unload_capacity_{t}} specifies the maximum number of containers that can be unloaded in a month.
- For each container kept in the yard until the subsequent month, there is a holding cost of $\var{holding_cost}.
- Due to space limitations, the yard can store a maximum of \var{max_container} containers at the end of any month.
- Initially, at the start of the first month, the yard has \var{init_container} containers.
- The yard should not contain any containers after the end of the last month.
- Additionally, loading containers onto ships necessitates the rental of cranes.
- A maximum of \var{num_cranes} cranes can be rented each month, each having a capacity to load \var{crane_capacity} containers.
- It costs \var{crane_cost} for each crane.

INPUT FORMAT: 

{
    "demands": [demand_{t} for t in 1, ..., T],
    "unload_costs": [unload_cost_{t} for t in 1, ..., T],
    "unload_capacity": [unload_capacity_{t} for t in 1, ..., T],
    "holding_cost": holding_cost,
    "max_container": max_container,
    "init_container": init_container,
    "num_cranes": num_cranes,
    "crane_capacity": crane_capacity,
    "crane_cost": crane_cost,
}

OBJECTIVE: Determine a strategy to minimize costs from unloading, storage, and crane rentals over the period.

OUTPUT INFO:

- \var{amount_{t}} indicates the number of containers unloaded for each month.
- \var{crane_{t}} specifies the number of cranes rented for each month.
- \var{total_cost} shows the total cost of the company over the period.

OUTPUT FORMAT:

{
    "containers_unloaded": [amount_{t} for t in 1, ..., T],
    "cranes_rented": [crane_{t} for t in 1, ..., T],
    "total_cost": total_cost
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Total number of months
    \item $demand_t$: Demand for containers by ships in month $t$, for $t = 1, \ldots, T$
    \item $unload\_cost_t$: Unloading cost per container in month $t$
    \item $unload\_capacity_t$: Maximum number of containers that can be unloaded in month $t$
    \item $holding\_cost$: Holding cost per container per month
    \item $max\_container$: Maximum number of containers that can be stored in the yard at the end of any month
    \item $init\_container$: Initial number of containers in the yard at the start of the first month
    \item $num\_cranes$: Maximum number of cranes that can be rented each month
    \item $crane\_capacity$: Capacity of each crane (number of containers it can load)
    \item $crane\_cost$: Cost to rent one crane
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_t$: Number of containers unloaded in month $t$
    \item $crane_t$: Number of cranes rented in month $t$
    \item $held_t$: Number of containers held in the yard at the end of month $t$
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_t \cdot amount_t + holding\_cost \cdot held_t + crane\_cost \cdot crane_t \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad amount_t \leq unload\_capacity_t, \quad \forall t \in \{1, \ldots, T\} \\
2. & \quad held_t = held_{t-1} + amount_t - demand_t, \quad \forall t \in \{1, \ldots, T\} \\
3. & \quad held_t \leq max\_container, \quad \forall t \in \{1, \ldots, T\} \\
4. & \quad held_t \geq 0, \quad \forall t \in \{1, \ldots, T\} \\
5. & \quad crane_t \cdot crane\_capacity \geq demand_t - held_{t-1}, \quad \forall t \in \{1, \ldots, T\} \\
6. & \quad crane_t \leq num\_cranes, \quad \forall t \in \{1, \ldots, T\} \\
7. & \quad held_0 = init\_container \\
8. & \quad held_T = 0
\end{align*}

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

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Total number of months
    \item $demand_t$: Demand for containers by ships in month $t$, for $t = 1, \ldots, T$
    \item $unload\_cost_t$: Unloading cost per container in month $t$
    \item $unload\_capacity_t$: Maximum number of containers that can be unloaded in month $t$
    \item $holding\_cost$: Holding cost per container per month
    \item $max\_container$: Maximum number of containers that can be stored in the yard at the end of any month
    \item $init\_container$: Initial number of containers in the yard at the start of the first month
    \item $num\_cranes$: Maximum number of cranes that can be rented each month
    \item $crane\_capacity$: Capacity of each crane (number of containers it can load)
    \item $crane\_cost$: Cost to rent one crane
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_t$: Number of containers unloaded in month $t$
    \item $crane_t$: Number of cranes rented in month $t$
    \item $held_t$: Number of containers held in the yard at the end of month $t$
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_t \cdot amount_t + holding\_cost \cdot held_t + crane\_cost \cdot crane_t \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad amount_t \leq unload\_capacity_t, \quad \forall t \in \{1, \ldots, T\} \\
2. & \quad held_t = held_{t-1} + amount_t - demand_t, \quad \forall t \in \{1, \ldots, T\} \\
3. & \quad held_t \leq max\_container, \quad \forall t \in \{1, \ldots, T\} \\
4. & \quad held_t \geq 0, \quad \forall t \in \{1, \ldots, T\} \\
5. & \quad crane_t \cdot crane\_capacity \geq demand_t - held_{t-1}, \quad \forall t \in \{1, \ldots, T\} \\
6. & \quad crane_t \leq num\_cranes, \quad \forall t \in \{1, \ldots, T\} \\
7. & \quad held_0 = init\_container \\
8. & \quad held_T = 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, upBound=data['NumCranes'], cat='Integer')
held = pulp.LpVariable.dicts("held", range(data['T'] + 1), lowBound=0)

#### Objective Function
total_cost = pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * held[t + 1] + data['CraneCost'] * crane[t] for t in range(data['T']))
problem += total_cost

#### Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unload_Capacity_Constraint_{t}"
    if t > 0:
        problem += held[t] == held[t - 1] + amount[t] - data['Demands'][t], f"Demand_Balance_Constraint_{t}"
    else:
        problem += held[0] == data['InitContainer'], f"Initial_Container_Constraint"

for t in range(data['T']):
    problem += held[t + 1] <= data['MaxContainer'], f"Max_Container_Constraint_{t}"
    problem += held[t + 1] >= 0, f"Non_Negative_Held_Constraint_{t}"
    if t > 0:
        problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t] - held[t], f"Crane_Capacity_Constraint_{t}"
        
#### Final constraint
problem += held[data['T']] == 0, "Final_Held_Constraint"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

