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

\section*{Mathematical Model for Container Unloading and Loading Optimization}

\textbf{Indices:}
\begin{itemize}
    \item $t = 1, 2, \ldots, T$: index for months
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_t$: demand for containers by ships in month $t$
    \item $unload\_cost_t$: cost to unload a single container in month $t$
    \item $unload\_capacity_t$: maximum number of containers that can be unloaded in month $t$
    \item $holding\_cost$: holding cost per container for each month
    \item $max\_container$: maximum containers that can be stored in the yard
    \item $init\_container$: initial number of containers in the yard
    \item $num\_cranes$: maximum number of cranes that can be rented each month
    \item $crane\_capacity$: capacity of each crane to load containers
    \item $crane\_cost$: cost to rent each crane
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $amount_t$: number of containers unloaded in month $t$
    \item $crane_t$: number of cranes rented in month $t$
    \item $total\_cost$: total cost over the period
    \item $containers\_in\_yard_t$: number of containers left in the yard at the end of month $t$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_cost = \sum_{t=1}^{T} (unload\_cost_t \cdot amount_t + holding\_cost \cdot containers\_in\_yard_t + crane\_cost \cdot crane_t)
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad containers\_in\_yard_1 = init\_container - amount_1 + demand_1 \\
2. & \quad containers\_in\_yard_t = containers\_in\_yard_{t-1} - amount_t + demand_t \quad \forall t \in \{2, \ldots, T\} \\
3. & \quad containers\_in\_yard_t \leq max\_container \quad \forall t \\
4. & \quad amount_t \leq unload\_capacity_t \quad \forall t \\
5. & \quad amount_t \geq demand_t \quad \forall t \\
6. & \quad crane_t \leq num\_cranes \quad \forall t \\
7. & \quad crane_t \cdot crane\_capacity \geq amount_t \quad \forall t \\
8. & \quad containers\_in\_yard_T = 0
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $containers\_unloaded = [amount_t \text{ for } t = 1, \ldots, T]$
    \item $cranes\_rented = [crane_t \text{ for } t = 1, \ldots, T]$
    \item $total\_cost$: total cost over the planning horizon
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

\section*{Mathematical Model for Container Unloading and Loading Optimization}

\textbf{Indices:}
\begin{itemize}
    \item $t = 1, 2, \ldots, T$: index for months
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $demand_t$: demand for containers by ships in month $t$
    \item $unload\_cost_t$: cost to unload a single container in month $t$
    \item $unload\_capacity_t$: maximum number of containers that can be unloaded in month $t$
    \item $holding\_cost$: holding cost per container for each month
    \item $max\_container$: maximum containers that can be stored in the yard
    \item $init\_container$: initial number of containers in the yard
    \item $num\_cranes$: maximum number of cranes that can be rented each month
    \item $crane\_capacity$: capacity of each crane to load containers
    \item $crane\_cost$: cost to rent each crane
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $amount_t$: number of containers unloaded in month $t$
    \item $crane_t$: number of cranes rented in month $t$
    \item $total\_cost$: total cost over the period
    \item $containers\_in\_yard_t$: number of containers left in the yard at the end of month $t$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_cost = \sum_{t=1}^{T} (unload\_cost_t \cdot amount_t + holding\_cost \cdot containers\_in\_yard_t + crane\_cost \cdot crane_t)
\]

\textbf{Constraints:}
\begin{align*}
1. & \quad containers\_in\_yard_1 = init\_container - amount_1 + demand_1 \\
2. & \quad containers\_in\_yard_t = containers\_in\_yard_{t-1} - amount_t + demand_t \quad \forall t \in \{2, \ldots, T\} \\
3. & \quad containers\_in\_yard_t \leq max\_container \quad \forall t \\
4. & \quad amount_t \leq unload\_capacity_t \quad \forall t \\
5. & \quad amount_t \geq demand_t \quad \forall t \\
6. & \quad crane_t \leq num\_cranes \quad \forall t \\
7. & \quad crane_t \cdot crane\_capacity \geq amount_t \quad \forall t \\
8. & \quad containers\_in\_yard_T = 0
\end{align*}

\textbf{Output Variables:}
\begin{itemize}
    \item $containers\_unloaded = [amount_t \text{ for } t = 1, \ldots, T]$
    \item $cranes\_rented = [crane_t \text{ for } t = 1, \ldots, T]$
    \item $total\_cost$: total cost over the planning horizon
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
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

#### Parameters
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

#### Create the problem
problem = pulp.LpProblem("Container_Unloading_Optimization", pulp.LpMinimize)

#### Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
containers_in_yard = pulp.LpVariable.dicts("containers_in_yard", range(1, T + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(unload_costs[t - 1] * amount[t] + holding_cost * containers_in_yard[t] + crane_cost * crane[t] for t in range(1, T + 1)), "Total_Cost"

#### Constraints
problem += containers_in_yard[1] == init_container - amount[1] + demands[0], "Initial_Containers_Yard"
for t in range(2, T + 1):
    problem += containers_in_yard[t] == containers_in_yard[t - 1] - amount[t] + demands[t - 1], f"Containers_Yard_{t}"
    problem += containers_in_yard[t] <= max_container, f"Max_Containers_Yard_{t}"
    problem += amount[t] <= unload_capacities[t - 1], f"Unload_Capacity_{t}"
    problem += amount[t] >= demands[t - 1], f"Demand_Satisfaction_{t}"
    problem += crane[t] * crane_capacity >= amount[t], f"Crane_Capacity_{t}"
    
problem += containers_in_yard[T] == 0, "Final_Containers_Yard"

#### Solve the problem
problem.solve()

#### Output results
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')
```

