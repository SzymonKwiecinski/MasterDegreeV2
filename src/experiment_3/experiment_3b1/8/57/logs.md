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

\subsection*{Parameters}
\begin{align*}
T & : \text{Total number of months} \\
demand_t & : \text{Demand for containers by ships in month } t, \; t = 1, \ldots, T \\
unload\_cost_t & : \text{Cost to unload a container in month } t \\
unload\_capacity_t & : \text{Maximum containers that can be unloaded in month } t \\
holding\_cost & : \text{Holding cost per container per month} \\
max\_container & : \text{Maximum containers that can be stored in the yard} \\
init\_container & : \text{Initial number of containers at the start of the first month} \\
num\_cranes & : \text{Maximum number of cranes that can be rented per month} \\
crane\_capacity & : \text{Loading capacity of each crane} \\
crane\_cost & : \text{Cost of renting one crane}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
amount_t & : \text{Number of containers unloaded in month } t, \; t = 1, \ldots, T \\
crane_t & : \text{Number of cranes rented in month } t, \; t = 1, \ldots, T \\
storage_t & : \text{Number of containers in the yard at the end of month } t, \; t = 1, \ldots, T
\end{align*}

\subsection*{Objective Function}
Minimize the total cost over the period:
\begin{align*}
\text{Minimize } \quad total\_cost & = \sum_{t=1}^{T} \left( unload\_cost_t \cdot amount_t + holding\_cost \cdot storage_t + crane\_cost \cdot crane_t \right)
\end{align*}

\subsection*{Constraints}
1. **Demand Satisfaction:**
\begin{align*}
amount_t + storage_{t-1} - storage_t & = demand_t, \quad t = 1, \ldots, T \\
storage_0 & = init\_container
\end{align*}

2. **Unloading Capacity:**
\begin{align*}
amount_t & \leq unload\_capacity_t, \quad t = 1, \ldots, T
\end{align*}

3. **Storage Capacity:**
\begin{align*}
storage_t & \leq max\_container, \quad t = 1, \ldots, T
\end{align*}

4. **Non-negativity:**
\begin{align*}
amount_t & \geq 0, \quad t = 1, \ldots, T \\
crane_t & \geq 0, \quad t = 1, \ldots, T \\
storage_t & \geq 0, \quad t = 1, \ldots, T
\end{align*}

5. **Crane Loading Capacity:**
\begin{align*}
crane_t \cdot crane\_capacity & \geq amount_t, \quad t = 1, \ldots, T
\end{align*}

6. **Cranes Rental Limit:**
\begin{align*}
crane_t & \leq num\_cranes, \quad t = 1, \ldots, T
\end{align*}

7. **Final Storage Condition:**
\begin{align*}
storage_T & = 0
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

\subsection*{Parameters}
\begin{align*}
T & : \text{Total number of months} \\
demand_t & : \text{Demand for containers by ships in month } t, \; t = 1, \ldots, T \\
unload\_cost_t & : \text{Cost to unload a container in month } t \\
unload\_capacity_t & : \text{Maximum containers that can be unloaded in month } t \\
holding\_cost & : \text{Holding cost per container per month} \\
max\_container & : \text{Maximum containers that can be stored in the yard} \\
init\_container & : \text{Initial number of containers at the start of the first month} \\
num\_cranes & : \text{Maximum number of cranes that can be rented per month} \\
crane\_capacity & : \text{Loading capacity of each crane} \\
crane\_cost & : \text{Cost of renting one crane}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
amount_t & : \text{Number of containers unloaded in month } t, \; t = 1, \ldots, T \\
crane_t & : \text{Number of cranes rented in month } t, \; t = 1, \ldots, T \\
storage_t & : \text{Number of containers in the yard at the end of month } t, \; t = 1, \ldots, T
\end{align*}

\subsection*{Objective Function}
Minimize the total cost over the period:
\begin{align*}
\text{Minimize } \quad total\_cost & = \sum_{t=1}^{T} \left( unload\_cost_t \cdot amount_t + holding\_cost \cdot storage_t + crane\_cost \cdot crane_t \right)
\end{align*}

\subsection*{Constraints}
1. **Demand Satisfaction:**
\begin{align*}
amount_t + storage_{t-1} - storage_t & = demand_t, \quad t = 1, \ldots, T \\
storage_0 & = init\_container
\end{align*}

2. **Unloading Capacity:**
\begin{align*}
amount_t & \leq unload\_capacity_t, \quad t = 1, \ldots, T
\end{align*}

3. **Storage Capacity:**
\begin{align*}
storage_t & \leq max\_container, \quad t = 1, \ldots, T
\end{align*}

4. **Non-negativity:**
\begin{align*}
amount_t & \geq 0, \quad t = 1, \ldots, T \\
crane_t & \geq 0, \quad t = 1, \ldots, T \\
storage_t & \geq 0, \quad t = 1, \ldots, T
\end{align*}

5. **Crane Loading Capacity:**
\begin{align*}
crane_t \cdot crane\_capacity & \geq amount_t, \quad t = 1, \ldots, T
\end{align*}

6. **Cranes Rental Limit:**
\begin{align*}
crane_t & \leq num\_cranes, \quad t = 1, \ldots, T
\end{align*}

7. **Final Storage Condition:**
\begin{align*}
storage_T & = 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, upBound=data['NumCranes'], cat='Integer')
storage = pulp.LpVariable.dicts("storage", range(data['T']), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * storage[t] + data['CraneCost'] * crane[t]
                       for t in range(data['T']))

#### Constraints
problem += storage[0] == data['InitContainer']

for t in range(data['T']):
    #### Demand Satisfaction
    if t > 0:
        problem += amount[t] + storage[t - 1] - storage[t] == data['Demands'][t]
    else:
        problem += amount[t] - storage[t] == data['Demands'][t]

    #### Unloading Capacity
    problem += amount[t] <= data['UnloadCapacity'][t]

    #### Storage Capacity
    problem += storage[t] <= data['MaxContainer']

    #### Crane Loading Capacity
    problem += crane[t] * data['CraneCapacity'] >= amount[t]

#### Final Storage Condition
problem += storage[data['T'] - 1] == 0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

