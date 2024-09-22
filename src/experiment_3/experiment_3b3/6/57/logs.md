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

\section*{Mathematical Model for Seaport Container Management}

% Variables
Let:
\begin{itemize}
    \item \( amount_t \): number of containers unloaded in month \( t \) 
    \item \( crane_t \): number of cranes rented in month \( t \)
    \item \( hold_t \): number of containers held in the yard at the end of month \( t \)
    \item \( total\_cost \): total cost over the period
\end{itemize}

% Parameters
Given parameters:
\begin{itemize}
    \item \( demand_t \): demand for containers by ships in month \( t \)
    \item \( unload\_cost_t \): unloading cost per container in month \( t \)
    \item \( unload\_capacity_t \): unloading capacity in month \( t \)
    \item \( holding\_cost \): holding cost per container per month
    \item \( max\_container \): maximum containers that can be stored in the yard
    \item \( init\_container \): initial number of containers in the yard
    \item \( num\_cranes \): maximum number of cranes that can be rented
    \item \( crane\_capacity \): capacity of each crane
    \item \( crane\_cost \): rental cost per crane
\end{itemize}

% Objective Function
\begin{align*}
    \text{Minimize } & total\_cost = \sum_{t=1}^{T} (unload\_cost_t \cdot amount_t + holding\_cost \cdot hold_t + crane\_cost \cdot crane_t) 
\end{align*}

% Constraints
Subject to:
\begin{align*}
    & amount_t \leq unload\_capacity_t, \quad \forall t \in [1, T] \quad \text{(Unloading Capacity)} \\
    & hold_t = hold_{t-1} + amount_t - demand_t, \quad \forall t \in [1, T] \\
    & hold_t \leq max\_container, \quad \forall t \in [1, T] \quad \text{(Yard Capacity)} \\
    & hold_0 = init\_container \quad \text{(Initial Condition)} \\
    & hold_T = 0 \quad \text{(Final Condition)} \\
    & crane_t \cdot crane\_capacity \geq amount_t, \quad \forall t \in [1, T] \quad \text{(Loading Capacity)} \\
    & crane_t \leq num\_cranes, \quad \forall t \in [1, T] \quad \text{(Cranes Limit)} \\
    & amount_t \geq 0, \quad crane_t \geq 0, \quad \forall t \in [1, T] \quad \text{(Non-negativity)}
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

\section*{Mathematical Model for Seaport Container Management}

% Variables
Let:
\begin{itemize}
    \item \( amount_t \): number of containers unloaded in month \( t \) 
    \item \( crane_t \): number of cranes rented in month \( t \)
    \item \( hold_t \): number of containers held in the yard at the end of month \( t \)
    \item \( total\_cost \): total cost over the period
\end{itemize}

% Parameters
Given parameters:
\begin{itemize}
    \item \( demand_t \): demand for containers by ships in month \( t \)
    \item \( unload\_cost_t \): unloading cost per container in month \( t \)
    \item \( unload\_capacity_t \): unloading capacity in month \( t \)
    \item \( holding\_cost \): holding cost per container per month
    \item \( max\_container \): maximum containers that can be stored in the yard
    \item \( init\_container \): initial number of containers in the yard
    \item \( num\_cranes \): maximum number of cranes that can be rented
    \item \( crane\_capacity \): capacity of each crane
    \item \( crane\_cost \): rental cost per crane
\end{itemize}

% Objective Function
\begin{align*}
    \text{Minimize } & total\_cost = \sum_{t=1}^{T} (unload\_cost_t \cdot amount_t + holding\_cost \cdot hold_t + crane\_cost \cdot crane_t) 
\end{align*}

% Constraints
Subject to:
\begin{align*}
    & amount_t \leq unload\_capacity_t, \quad \forall t \in [1, T] \quad \text{(Unloading Capacity)} \\
    & hold_t = hold_{t-1} + amount_t - demand_t, \quad \forall t \in [1, T] \\
    & hold_t \leq max\_container, \quad \forall t \in [1, T] \quad \text{(Yard Capacity)} \\
    & hold_0 = init\_container \quad \text{(Initial Condition)} \\
    & hold_T = 0 \quad \text{(Final Condition)} \\
    & crane_t \cdot crane\_capacity \geq amount_t, \quad \forall t \in [1, T] \quad \text{(Loading Capacity)} \\
    & crane_t \leq num\_cranes, \quad \forall t \in [1, T] \quad \text{(Cranes Limit)} \\
    & amount_t \geq 0, \quad crane_t \geq 0, \quad \forall t \in [1, T] \quad \text{(Non-negativity)}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Load data
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
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

#### Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0) for t in range(data['T'])]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, cat=pulp.LpInteger) for t in range(data['T'])]
hold = [pulp.LpVariable(f'hold_{t}', lowBound=0) for t in range(data['T'] + 1)]

#### Objective function
total_cost = pulp.lpSum(
    [data['UnloadCosts'][t] * amount[t] +
     data['HoldingCost'] * hold[t + 1] +
     data['CraneCost'] * crane[t] for t in range(data['T'])]
)
problem += total_cost

#### Constraints
problem += hold[0] == data['InitContainer'], "Initial_Condition"
problem += hold[data['T']] == 0, "Final_Condition"

for t in range(data['T']):
    #### Unloading Capacity
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unloading_Capacity_{t}"
    
    #### Yard Capacity
    problem += hold[t + 1] <= data['MaxContainer'], f"Yard_Capacity_{t}"
    
    #### Inventory Balance
    problem += hold[t + 1] == hold[t] + amount[t] - data['Demands'][t], f"Inventory_Balance_{t}"
    
    #### Loading Capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t], f"Loading_Capacity_{t}"
    
    #### Cranes Limit
    problem += crane[t] <= data['NumCranes'], f"Cranes_Limit_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

