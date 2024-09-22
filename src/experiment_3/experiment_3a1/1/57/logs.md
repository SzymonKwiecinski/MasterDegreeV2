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

\title{Mixed Integer Programming Model for Container Handling at a Seaport}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Let:
\begin{itemize}
    \item $T$: Total number of months
    \item $demand_{t}$: Demand for containers by ships in month $t$
    \item $unload\_cost_{t}$: Unloading cost per container in month $t$
    \item $unload\_capacity_{t}$: Maximum containers that can be unloaded in month $t$
    \item $holding\_cost$: Holding cost per container
    \item $max\_container$: Maximum containers that can be stored in the yard at the end of any month
    \item $init\_container$: Initial number of containers at the start of month 1
    \item $num\_cranes$: Maximum number of cranes that can be rented per month
    \item $crane\_capacity$: Number of containers each crane can load
    \item $crane\_cost$: Cost to rent each crane
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_{t}$: Number of containers unloaded in month $t$, for $t=1,\ldots,T$
    \item $crane_{t}$: Number of cranes rented in month $t$, for $t=1,\ldots,T$
    \item $containers_{t}$: Number of containers in the yard at the end of month $t$, for $t=1,\ldots,T$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost over the period:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_{t} \cdot amount_{t} + holding\_cost \cdot containers_{t} + crane\_cost \cdot crane_{t} \right)
\]

\subsection*{Constraints}
\begin{align}
1. & \quad containers_{t} = init\_container + \sum_{i=1}^{t} amount_{i} - \sum_{j=1}^{t} crane_{j} \cdot crane\_capacity \quad \forall t \\
2. & \quad containers_{t} \leq max\_container \quad \forall t \\
3. & \quad amount_{t} \leq unload\_capacity_{t}  \quad \forall t \\
4. & \quad amount_{t} \geq demand_{t} \quad \forall t \\
5. & \quad crane_{t} \leq num\_cranes \quad \forall t \\
6. & \quad containers_{T} = 0 \\ 
\end{align}

\subsection*{Output}
The outputs of the model will be:
\begin{itemize}
    \item $containers\_unloaded = [amount_{t} \text{ for } t=1,\ldots,T]$
    \item $cranes\_rented = [crane_{t} \text{ for } t=1,\ldots,T]$
    \item $total\_cost = \text{Total Cost}$
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

\title{Mixed Integer Programming Model for Container Handling at a Seaport}
\author{}
\date{}
\maketitle

\section*{Problem Formulation}

Let:
\begin{itemize}
    \item $T$: Total number of months
    \item $demand_{t}$: Demand for containers by ships in month $t$
    \item $unload\_cost_{t}$: Unloading cost per container in month $t$
    \item $unload\_capacity_{t}$: Maximum containers that can be unloaded in month $t$
    \item $holding\_cost$: Holding cost per container
    \item $max\_container$: Maximum containers that can be stored in the yard at the end of any month
    \item $init\_container$: Initial number of containers at the start of month 1
    \item $num\_cranes$: Maximum number of cranes that can be rented per month
    \item $crane\_capacity$: Number of containers each crane can load
    \item $crane\_cost$: Cost to rent each crane
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $amount_{t}$: Number of containers unloaded in month $t$, for $t=1,\ldots,T$
    \item $crane_{t}$: Number of cranes rented in month $t$, for $t=1,\ldots,T$
    \item $containers_{t}$: Number of containers in the yard at the end of month $t$, for $t=1,\ldots,T$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost over the period:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_{t} \cdot amount_{t} + holding\_cost \cdot containers_{t} + crane\_cost \cdot crane_{t} \right)
\]

\subsection*{Constraints}
\begin{align}
1. & \quad containers_{t} = init\_container + \sum_{i=1}^{t} amount_{i} - \sum_{j=1}^{t} crane_{j} \cdot crane\_capacity \quad \forall t \\
2. & \quad containers_{t} \leq max\_container \quad \forall t \\
3. & \quad amount_{t} \leq unload\_capacity_{t}  \quad \forall t \\
4. & \quad amount_{t} \geq demand_{t} \quad \forall t \\
5. & \quad crane_{t} \leq num\_cranes \quad \forall t \\
6. & \quad containers_{T} = 0 \\ 
\end{align}

\subsection*{Output}
The outputs of the model will be:
\begin{itemize}
    \item $containers\_unloaded = [amount_{t} \text{ for } t=1,\ldots,T]$
    \item $cranes\_rented = [crane_{t} \text{ for } t=1,\ldots,T]$
    \item $total\_cost = \text{Total Cost}$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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

#### Define the problem
problem = pulp.LpProblem("Container_Handling_Seaport", pulp.LpMinimize)

#### Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]
containers = [pulp.LpVariable(f'containers_{t}', lowBound=0, upBound=data['MaxContainer'], cat='Continuous') for t in range(data['T'])]

#### Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] + data['HoldingCost'] * containers[t] + data['CraneCost'] * crane[t] for t in range(data['T']))

#### Constraints
for t in range(data['T']):
    if t == 0:
        problem += containers[t] == data['InitContainer'] + amount[t]
    else:
        problem += containers[t] == data['InitContainer'] + pulp.lpSum(amount[i] for i in range(t + 1)) - pulp.lpSum(crane[j] * data['CraneCapacity'] for j in range(t + 1))

    problem += containers[t] <= data['MaxContainer']
    problem += amount[t] <= data['UnloadCapacity'][t]
    problem += amount[t] >= data['Demands'][t]

problem += containers[data['T'] - 1] == 0  #### Last month containers must be zero

#### Solve the problem
problem.solve()

#### Output results
containers_unloaded = [amount[t].varValue for t in range(data['T'])]
cranes_rented = [crane[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')
```

