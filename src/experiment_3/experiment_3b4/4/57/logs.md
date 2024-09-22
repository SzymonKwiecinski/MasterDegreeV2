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
To model this Mixed-Integer Programming (MIP) problem, we need to define decision variables, objective function, and constraints. Let's proceed with the formulation:

######### Decision Variables

- \( \text{amount}_{t} \): Number of containers unloaded in month \( t \).
- \( \text{hold}_{t} \): Number of containers held in the yard at the end of month \( t \).
- \( \text{crane}_{t} \): Number of cranes rented in month \( t \).

######### Objective Function

We want to minimize the total cost over the planning horizon, which includes unloading costs, holding costs, and crane rental costs.

######### Constraints

1. **Demand Fulfillment**: For each month \( t \), the demand must be fulfilled.
   \[
   \text{amount}_t + \text{hold}_{t-1} - \text{hold}_{t} \geq \text{demand}_{t}, \quad \forall t
   \]

2. **Unloading Capacity**: Do not exceed the unloading capacity per month.
   \[
   0 \leq \text{amount}_{t} \leq \text{unload\_capacity}_{t}, \quad \forall t
   \]

3. **Yard Capacity**: The number of containers held in the yard cannot exceed the maximum capacity.
   \[
   0 \leq \text{hold}_{t} \leq \text{max\_container}, \quad \forall t
   \]

4. **Initial Condition**: At the start of the first month, there is a known initial number of containers.
   \[
   \text{hold}_0 = \text{init\_container}
   \]

5. **Final Condition**: At the end of the last month, the yard should be empty.
   \[
   \text{hold}_{T} = 0
   \]

6. **Cranes for Loading**: Ensure that the number of cranes rented and their capacity can handle the demand.
   \[
   \text{crane}_t \times \text{crane\_capacity} \geq \text{demand}_{t}, \quad \forall t
   \]
   \[
   0 \leq \text{crane}_t \leq \text{num\_cranes}, \quad \forall t
   \]

Let's write the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $\text{demand}_{t}$: Demand for containers in month $t$.
    \item $\text{unload\_cost}_{t}$: Unloading cost per container in month $t$.
    \item $\text{unload\_capacity}_{t}$: Maximum number of containers to unload in month $t$.
    \item $\text{holding\_cost}$: Cost of holding a container for a month.
    \item $\text{max\_container}$: Maximum number of containers that can be held in the yard.
    \item $\text{init\_container}$: Initial number of containers in the yard.
    \item $\text{num\_cranes}$: Maximum number of cranes available for rent.
    \item $\text{crane\_capacity}$: Capacity of each crane.
    \item $\text{crane\_cost}$: Cost of renting each crane.
    \item $T$: Number of months in the planning horizon.
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    & \text{amount}_{t}: \text{Number of containers unloaded in month } t. \\
    & \text{hold}_{t}: \text{Number of containers held in the yard at the end of month } t. \\
    & \text{crane}_{t}: \text{Number of cranes rented in month } t.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \times \text{amount}_{t} + \text{holding\_cost} \times \text{hold}_{t} + \text{crane\_cost} \times \text{crane}_{t} \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{amount}_t + \text{hold}_{t-1} - \text{hold}_{t} \geq \text{demand}_{t}, \quad \forall t \\
    & 0 \leq \text{amount}_{t} \leq \text{unload\_capacity}_{t}, \quad \forall t \\
    & 0 \leq \text{hold}_{t} \leq \text{max\_container}, \quad \forall t \\
    & \text{hold}_0 = \text{init\_container} \\
    & \text{hold}_{T} = 0 \\
    & \text{crane}_t \times \text{crane\_capacity} \geq \text{demand}_{t}, \quad \forall t \\
    & 0 \leq \text{crane}_{t} \leq \text{num\_cranes}, \quad \forall t
\end{align*}

\end{document}
```

This LaTeX code provides a comprehensive mathematical model for the seaport operations problem.

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
    \item $\text{demand}_{t}$: Demand for containers in month $t$.
    \item $\text{unload\_cost}_{t}$: Unloading cost per container in month $t$.
    \item $\text{unload\_capacity}_{t}$: Maximum number of containers to unload in month $t$.
    \item $\text{holding\_cost}$: Cost of holding a container for a month.
    \item $\text{max\_container}$: Maximum number of containers that can be held in the yard.
    \item $\text{init\_container}$: Initial number of containers in the yard.
    \item $\text{num\_cranes}$: Maximum number of cranes available for rent.
    \item $\text{crane\_capacity}$: Capacity of each crane.
    \item $\text{crane\_cost}$: Cost of renting each crane.
    \item $T$: Number of months in the planning horizon.
\end{itemize}

\subsection*{Decision Variables}
\begin{align*}
    & \text{amount}_{t}: \text{Number of containers unloaded in month } t. \\
    & \text{hold}_{t}: \text{Number of containers held in the yard at the end of month } t. \\
    & \text{crane}_{t}: \text{Number of cranes rented in month } t.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_{t} \times \text{amount}_{t} + \text{holding\_cost} \times \text{hold}_{t} + \text{crane\_cost} \times \text{crane}_{t} \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \text{amount}_t + \text{hold}_{t-1} - \text{hold}_{t} \geq \text{demand}_{t}, \quad \forall t \\
    & 0 \leq \text{amount}_{t} \leq \text{unload\_capacity}_{t}, \quad \forall t \\
    & 0 \leq \text{hold}_{t} \leq \text{max\_container}, \quad \forall t \\
    & \text{hold}_0 = \text{init\_container} \\
    & \text{hold}_{T} = 0 \\
    & \text{crane}_t \times \text{crane\_capacity} \geq \text{demand}_{t}, \quad \forall t \\
    & 0 \leq \text{crane}_{t} \leq \text{num\_cranes}, \quad \forall t
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

#### Unpack data
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

#### Problem
problem = pulp.LpProblem("Container_Unloading", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(T), lowBound=0)
hold = pulp.LpVariable.dicts("Hold", range(T+1), lowBound=0, upBound=max_container)
crane = pulp.LpVariable.dicts("Crane", range(T), lowBound=0, upBound=num_cranes)

#### Objective Function
problem += pulp.lpSum(unload_costs[t] * amount[t] + holding_cost * hold[t+1] + crane_cost * crane[t] for t in range(T))

#### Constraints
problem += hold[0] == init_container
for t in range(T):
    problem += amount[t] + hold[t] - hold[t+1] >= demands[t]
    problem += amount[t] <= unload_capacity[t]
    problem += crane[t] * crane_capacity >= demands[t]
problem += hold[T] == 0

#### Solve
problem.solve()

#### Objective Value
objective_value = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{objective_value}</OBJ>')
```

