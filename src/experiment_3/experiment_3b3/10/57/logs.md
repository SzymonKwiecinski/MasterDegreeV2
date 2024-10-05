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

\section*{Mathematical Model for Container Management at a Seaport}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: number of months
    \item $demand_{t}$: demand for containers by ships in month $t$ for $t = 1, \ldots, T$
    \item $unload\_cost_{t}$: unloading cost per container in month $t$
    \item $unload\_capacity_{t}$: unloading capacity in month $t$
    \item $holding\_cost$: holding cost per container per month
    \item $max\_container$: maximum number of containers the yard can store at the end of any month
    \item $init\_container$: initial number of containers in the yard at month 1
    \item $num\_cranes$: maximum number of cranes that can be rented each month
    \item $crane\_capacity$: capacity of each crane for loading containers
    \item $crane\_cost$: rental cost per crane per month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_{t}$: number of containers unloaded in month $t$
    \item $crane_{t}$: number of cranes rented in month $t$
    \item $storage_{t}$: number of containers stored in the yard at the end of month $t$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_{t} \cdot amount_{t} + holding\_cost \cdot storage_{t} + crane\_cost \cdot crane_{t} \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{1. Demand fulfillment:} & \quad amount_{t} \geq demand_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{2. Unloading capacity:} & \quad amount_{t} \leq unload\_capacity_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{3. Crane capacity:} & \quad crane_{t} \cdot crane\_capacity \geq amount_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{4. Crane rental limit:} & \quad crane_{t} \leq num\_cranes \quad \forall t \in \{1, \ldots, T\} \\
    \text{5. Storage balance:} & \quad storage_{t} = storage_{t-1} + amount_{t} - demand_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{6. Initial storage:} & \quad storage_{1} = init\_container \\
    \text{7. Maximum storage:} & \quad storage_{t} \leq max\_container \quad \forall t \in \{1, \ldots, T\} \\
    \text{8. Final storage:} & \quad storage_{T} = 0
\end{align}

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

\section*{Mathematical Model for Container Management at a Seaport}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: number of months
    \item $demand_{t}$: demand for containers by ships in month $t$ for $t = 1, \ldots, T$
    \item $unload\_cost_{t}$: unloading cost per container in month $t$
    \item $unload\_capacity_{t}$: unloading capacity in month $t$
    \item $holding\_cost$: holding cost per container per month
    \item $max\_container$: maximum number of containers the yard can store at the end of any month
    \item $init\_container$: initial number of containers in the yard at month 1
    \item $num\_cranes$: maximum number of cranes that can be rented each month
    \item $crane\_capacity$: capacity of each crane for loading containers
    \item $crane\_cost$: rental cost per crane per month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_{t}$: number of containers unloaded in month $t$
    \item $crane_{t}$: number of cranes rented in month $t$
    \item $storage_{t}$: number of containers stored in the yard at the end of month $t$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_{t} \cdot amount_{t} + holding\_cost \cdot storage_{t} + crane\_cost \cdot crane_{t} \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{1. Demand fulfillment:} & \quad amount_{t} \geq demand_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{2. Unloading capacity:} & \quad amount_{t} \leq unload\_capacity_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{3. Crane capacity:} & \quad crane_{t} \cdot crane\_capacity \geq amount_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{4. Crane rental limit:} & \quad crane_{t} \leq num\_cranes \quad \forall t \in \{1, \ldots, T\} \\
    \text{5. Storage balance:} & \quad storage_{t} = storage_{t-1} + amount_{t} - demand_{t} \quad \forall t \in \{1, \ldots, T\} \\
    \text{6. Initial storage:} & \quad storage_{1} = init\_container \\
    \text{7. Maximum storage:} & \quad storage_{t} \leq max\_container \quad \forall t \in \{1, \ldots, T\} \\
    \text{8. Final storage:} & \quad storage_{T} = 0
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

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

#### Model
problem = pulp.LpProblem("Container_Management", pulp.LpMinimize)

#### Decision variables
amount = pulp.LpVariable.dicts("Amount", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpInteger)
crane = pulp.LpVariable.dicts("Crane", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpInteger)

#### Objective function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] +
                      data['HoldingCost'] * storage[t] +
                      data['CraneCost'] * crane[t] for t in range(1, data['T'] + 1))

#### Constraints
for t in range(1, data['T'] + 1):
    #### Demand fulfillment
    problem += amount[t] >= data['Demands'][t-1]
    
    #### Unloading capacity
    problem += amount[t] <= data['UnloadCapacity'][t-1]
    
    #### Crane capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t]
    
    #### Storage balance
    if t == 1:
        problem += storage[t] == data['InitContainer'] + amount[t] - data['Demands'][t-1]
    else:
        problem += storage[t] == storage[t-1] + amount[t] - data['Demands'][t-1]
    
    #### Maximum storage
    problem += storage[t] <= data['MaxContainer']

#### Final storage should be zero
problem += storage[data['T']] == 0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


