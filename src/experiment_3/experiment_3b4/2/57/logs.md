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
To model this problem, we will create a mixed integer programming (MIP) formulation. Our goal is to find a strategy that minimizes the total cost arising from unloading containers, storing them, and renting cranes over the given time period. Here's the mathematical model represented in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost over the period.

\begin{align*}
\text{Minimize } & \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \times \text{amount}_{t} + \text{holding\_cost} \times \text{storage}_{t} + \text{crane\_cost} \times \text{crane}_{t} \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \text{amount}_{t} \leq \text{unload\_capacity}_{t}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{t} = \text{storage}_{t-1} + \text{amount}_{t} - \text{demand}_{t}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{t} \leq \text{max\_container}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{0} = \text{init\_container}, \\
& \text{storage}_{T} = 0, \\
& \text{demand}_{t} \leq \text{crane\_capacity} \times \text{crane}_{t}, & \forall t = 1, \ldots, T, \\
& \text{crane}_{t} \leq \text{num\_cranes}, & \forall t = 1, \ldots, T, \\
& \text{amount}_{t}, \text{storage}_{t}, \text{crane}_{t} \geq 0, & \forall t = 1, \ldots, T, \\
& \text{crane}_{t} \in \mathbb{Z}, & \forall t = 1, \ldots, T.
\end{align*}

\textbf{Variables:}

\begin{itemize}
    \item $\text{amount}_{t}$: Number of containers unloaded in month $t$.
    \item $\text{storage}_{t}$: Number of containers stored in the yard at the end of month $t$.
    \item $\text{crane}_{t}$: Number of cranes rented in month $t$.
\end{itemize}

\end{document}
```

This formulation includes constraints to ensure:

1. The number of containers unloaded does not exceed the unloading capacity for each month.
2. The storage updates as per the number of containers unloaded, stored from the previous month, and those loaded onto ships (demands fulfilled).
3. Storage must not exceed the maximum container capacity in any month.
4. The initial storage condition at the start and the requirement to have zero containers at the end.
5. The number of cranes rented must be sufficient to meet the demand but does not exceed the available cranes each month.
6. Non-negativity and integrality constraints for the relevant variables.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost over the period.

\begin{align*}
\text{Minimize } & \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \times \text{amount}_{t} + \text{holding\_cost} \times \text{storage}_{t} + \text{crane\_cost} \times \text{crane}_{t} \right)
\end{align*}

\textbf{Subject to:}

\begin{align*}
& \text{amount}_{t} \leq \text{unload\_capacity}_{t}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{t} = \text{storage}_{t-1} + \text{amount}_{t} - \text{demand}_{t}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{t} \leq \text{max\_container}, & \forall t = 1, \ldots, T, \\
& \text{storage}_{0} = \text{init\_container}, \\
& \text{storage}_{T} = 0, \\
& \text{demand}_{t} \leq \text{crane\_capacity} \times \text{crane}_{t}, & \forall t = 1, \ldots, T, \\
& \text{crane}_{t} \leq \text{num\_cranes}, & \forall t = 1, \ldots, T, \\
& \text{amount}_{t}, \text{storage}_{t}, \text{crane}_{t} \geq 0, & \forall t = 1, \ldots, T, \\
& \text{crane}_{t} \in \mathbb{Z}, & \forall t = 1, \ldots, T.
\end{align*}

\textbf{Variables:}

\begin{itemize}
    \item $\text{amount}_{t}$: Number of containers unloaded in month $t$.
    \item $\text{storage}_{t}$: Number of containers stored in the yard at the end of month $t$.
    \item $\text{crane}_{t}$: Number of cranes rented in month $t$.
\end{itemize}

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

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Define variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", range(data['T'] + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, cat='Integer')

#### Objective function
problem += pulp.lpSum([
    data['UnloadCosts'][t] * amount[t] +
    data['HoldingCost'] * storage[t] +
    data['CraneCost'] * crane[t]
    for t in range(data['T'])
])

#### Constraints
#### Initial storage
problem += storage[0] == data['InitContainer']

#### Final storage must be zero
problem += storage[data['T']] == 0

for t in range(data['T']):
    #### Amount constraints
    problem += amount[t] <= data['UnloadCapacity'][t]
    
    #### Storage balance constraint
    problem += storage[t + 1] == storage[t] + amount[t] - data['Demands'][t]
    
    #### Max container in storage
    problem += storage[t] <= data['MaxContainer']

    #### Crane capacity constraint
    problem += data['Demands'][t] <= data['CraneCapacity'] * crane[t]

    #### Max number of cranes
    problem += crane[t] <= data['NumCranes']

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

