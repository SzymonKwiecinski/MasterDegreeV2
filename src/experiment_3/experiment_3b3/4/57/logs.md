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

\subsection*{Indices}
\begin{itemize}
    \item \( t \): month index, \( t = 1, 2, \ldots, T \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{demand}_{t} \): demand for containers by ships in month \( t \) 
    \item \( \text{unload\_cost}_{t} \): unloading cost per container in month \( t \)
    \item \( \text{unload\_capacity}_{t} \): maximum number of containers that can be unloaded in month \( t \)
    \item \( \text{holding\_cost} \): holding cost for each container in the yard
    \item \( \text{max\_container} \): maximum storage capacity of the yard
    \item \( \text{init\_container} \): initial number of containers in the yard at month 1
    \item \( \text{num\_cranes} \): maximum number of cranes that can be rented each month
    \item \( \text{crane\_capacity} \): capacity of each crane
    \item \( \text{crane\_cost} \): rental cost of each crane
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( \text{amount}_{t} \): number of containers unloaded in month \( t \)
    \item \( \text{crane}_{t} \): number of cranes rented in month \( t \)
    \item \( \text{total\_cost} \): total cost incurred over the period
    \item \( \text{hold}_{t} \): number of containers held in the yard at the end of month \( t \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{total\_cost} = \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \cdot \text{amount}_{t} + \text{holding\_cost} \cdot \text{hold}_{t} + \text{crane\_cost} \cdot \text{crane}_{t} \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \text{amount}_{t} \leq \text{unload\_capacity}_{t}, \quad \forall t \\
2. & \quad \text{hold}_{t-1} + \text{amount}_{t} - \text{demand}_{t} = \text{hold}_{t}, \quad \forall t \\
3. & \quad 0 \leq \text{hold}_{t} \leq \text{max\_container}, \quad \forall t \\
4. & \quad \text{hold}_{T} = 0 \\
5. & \quad \text{crane}_{t} \cdot \text{crane\_capacity} \geq \text{amount}_{t}, \quad \forall t \\
6. & \quad 0 \leq \text{crane}_{t} \leq \text{num\_cranes}, \quad \forall t \\
7. & \quad \text{amount}_{1} = \text{init\_container} - \text{hold}_{1} \\
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

\subsection*{Indices}
\begin{itemize}
    \item \( t \): month index, \( t = 1, 2, \ldots, T \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{demand}_{t} \): demand for containers by ships in month \( t \) 
    \item \( \text{unload\_cost}_{t} \): unloading cost per container in month \( t \)
    \item \( \text{unload\_capacity}_{t} \): maximum number of containers that can be unloaded in month \( t \)
    \item \( \text{holding\_cost} \): holding cost for each container in the yard
    \item \( \text{max\_container} \): maximum storage capacity of the yard
    \item \( \text{init\_container} \): initial number of containers in the yard at month 1
    \item \( \text{num\_cranes} \): maximum number of cranes that can be rented each month
    \item \( \text{crane\_capacity} \): capacity of each crane
    \item \( \text{crane\_cost} \): rental cost of each crane
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( \text{amount}_{t} \): number of containers unloaded in month \( t \)
    \item \( \text{crane}_{t} \): number of cranes rented in month \( t \)
    \item \( \text{total\_cost} \): total cost incurred over the period
    \item \( \text{hold}_{t} \): number of containers held in the yard at the end of month \( t \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{total\_cost} = \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \cdot \text{amount}_{t} + \text{holding\_cost} \cdot \text{hold}_{t} + \text{crane\_cost} \cdot \text{crane}_{t} \right)
\]

\subsection*{Constraints}
\begin{align*}
1. & \quad \text{amount}_{t} \leq \text{unload\_capacity}_{t}, \quad \forall t \\
2. & \quad \text{hold}_{t-1} + \text{amount}_{t} - \text{demand}_{t} = \text{hold}_{t}, \quad \forall t \\
3. & \quad 0 \leq \text{hold}_{t} \leq \text{max\_container}, \quad \forall t \\
4. & \quad \text{hold}_{T} = 0 \\
5. & \quad \text{crane}_{t} \cdot \text{crane\_capacity} \geq \text{amount}_{t}, \quad \forall t \\
6. & \quad 0 \leq \text{crane}_{t} \leq \text{num\_cranes}, \quad \forall t \\
7. & \quad \text{amount}_{1} = \text{init\_container} - \text{hold}_{1} \\
\end{align*}

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

#### Indices
T = data['T']

#### Problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, cat='Integer')
hold = pulp.LpVariable.dicts("hold", range(T), lowBound=0, upBound=data['MaxContainer'], cat='Continuous')

#### Objective Function
total_cost = pulp.lpSum(
    data['UnloadCosts'][t] * amount[t] + 
    data['HoldingCost'] * hold[t] + 
    data['CraneCost'] * crane[t]
    for t in range(T)
)
problem += total_cost

#### Constraints
for t in range(T):
    #### Constraint 1: amount_t <= unload_capacity_t
    problem += amount[t] <= data['UnloadCapacity'][t]

    #### Constraint 2: hold_{t-1} + amount_t - demand_t = hold_t
    if t == 0:
        problem += data['InitContainer'] + amount[t] - data['Demands'][t] == hold[t]
    else:
        problem += hold[t-1] + amount[t] - data['Demands'][t] == hold[t]

    #### Constraint 5: crane_t * crane_capacity >= amount_t
    problem += crane[t] * data['CraneCapacity'] >= amount[t]
    
    #### Constraint 6: 0 <= crane_t <= num_cranes
    problem += crane[t] <= data['NumCranes']

#### Constraint 4: hold_T = 0
problem += hold[T - 1] == 0

#### Constraint 7: amount_1 = init_container - hold_1
problem += amount[0] == data['InitContainer'] - hold[0]

#### Solve
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

