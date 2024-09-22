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

\section*{Mathematical Model for Seaport Operations}

We are tasked with developing a Mixed-Integer Programming (MIP) model to minimize the cost associated with unloading, holding, and loading shipping containers at a seaport. The model operates over a time horizon of \( T \) months.

\subsection*{Indices}
\begin{align*}
t & : \text{Index for months, } t = 1, 2, \ldots, T
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{demand}_t & : \text{Demand for containers by ships in month } t \\
\text{unload\_cost}_t & : \text{Cost to unload a single container in month } t \\
\text{unload\_capacity}_t & : \text{Maximum number of containers that can be unloaded in month } t \\
\text{holding\_cost} & : \text{Holding cost per container per month} \\
\text{max\_container} & : \text{Maximum containers the yard can store at the end of any month} \\
\text{init\_container} & : \text{Initial number of containers in the yard} \\
\text{num\_cranes} & : \text{Maximum number of cranes that can be rented each month} \\
\text{crane\_capacity} & : \text{Capacity of a single crane in loading containers} \\
\text{crane\_cost} & : \text{Cost to rent a single crane}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{amount}_t & : \text{Number of containers unloaded in month } t \\
\text{crane}_t & : \text{Number of cranes rented in month } t \\
\text{yard}_t & : \text{Number of containers in the yard at the end of month } t
\end{align*}

\subsection*{Objective Function}

Minimize the total cost:
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_t \times \text{amount}_t + \text{holding\_cost} \times \text{yard}_t + \text{crane\_cost} \times \text{crane}_t \right)
\]

\subsection*{Constraints}

\begin{align*}
1. & \quad \text{amount}_t \leq \text{unload\_capacity}_t, \quad \forall t \\
2. & \quad \text{yard}_{t-1} + \text{amount}_t - \text{demand}_t = \text{yard}_t, \quad \forall t \\
3. & \quad \text{crane}_t \times \text{crane\_capacity} \geq \text{demand}_t, \quad \forall t \\
4. & \quad \text{yard}_t \leq \text{max\_container}, \quad \forall t \\
5. & \quad \text{yard}_T = 0 \\
6. & \quad \text{crane}_t \leq \text{num\_cranes}, \quad \forall t \\
7. & \quad \text{yard}_0 = \text{init\_container}
\end{align*}

\subsection*{Variable Domains}

\begin{align*}
\text{amount}_t & \geq 0 \quad \text{and integer, } \forall t \\
\text{crane}_t & \geq 0 \quad \text{and integer, } \forall t \\
\text{yard}_t & \geq 0 \quad \text{and integer, } \forall t
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

\section*{Mathematical Model for Seaport Operations}

We are tasked with developing a Mixed-Integer Programming (MIP) model to minimize the cost associated with unloading, holding, and loading shipping containers at a seaport. The model operates over a time horizon of \( T \) months.

\subsection*{Indices}
\begin{align*}
t & : \text{Index for months, } t = 1, 2, \ldots, T
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{demand}_t & : \text{Demand for containers by ships in month } t \\
\text{unload\_cost}_t & : \text{Cost to unload a single container in month } t \\
\text{unload\_capacity}_t & : \text{Maximum number of containers that can be unloaded in month } t \\
\text{holding\_cost} & : \text{Holding cost per container per month} \\
\text{max\_container} & : \text{Maximum containers the yard can store at the end of any month} \\
\text{init\_container} & : \text{Initial number of containers in the yard} \\
\text{num\_cranes} & : \text{Maximum number of cranes that can be rented each month} \\
\text{crane\_capacity} & : \text{Capacity of a single crane in loading containers} \\
\text{crane\_cost} & : \text{Cost to rent a single crane}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{amount}_t & : \text{Number of containers unloaded in month } t \\
\text{crane}_t & : \text{Number of cranes rented in month } t \\
\text{yard}_t & : \text{Number of containers in the yard at the end of month } t
\end{align*}

\subsection*{Objective Function}

Minimize the total cost:
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_t \times \text{amount}_t + \text{holding\_cost} \times \text{yard}_t + \text{crane\_cost} \times \text{crane}_t \right)
\]

\subsection*{Constraints}

\begin{align*}
1. & \quad \text{amount}_t \leq \text{unload\_capacity}_t, \quad \forall t \\
2. & \quad \text{yard}_{t-1} + \text{amount}_t - \text{demand}_t = \text{yard}_t, \quad \forall t \\
3. & \quad \text{crane}_t \times \text{crane\_capacity} \geq \text{demand}_t, \quad \forall t \\
4. & \quad \text{yard}_t \leq \text{max\_container}, \quad \forall t \\
5. & \quad \text{yard}_T = 0 \\
6. & \quad \text{crane}_t \leq \text{num\_cranes}, \quad \forall t \\
7. & \quad \text{yard}_0 = \text{init\_container}
\end{align*}

\subsection*{Variable Domains}

\begin{align*}
\text{amount}_t & \geq 0 \quad \text{and integer, } \forall t \\
\text{crane}_t & \geq 0 \quad \text{and integer, } \forall t \\
\text{yard}_t & \geq 0 \quad \text{and integer, } \forall t
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
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
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

#### Decision Variables
amount = pulp.LpVariable.dicts("amount", range(data['T']), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("crane", range(data['T']), lowBound=0, cat='Integer')
yard = pulp.LpVariable.dicts("yard", range(data['T'] + 1), lowBound=0, cat='Integer')

#### Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * amount[t] +
                       data['HoldingCost'] * yard[t] +
                       data['CraneCost'] * crane[t] 
                       for t in range(data['T'])), "Total Cost"

#### Constraints
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t], f"Unload_Capacity_Constraint_{t+1}"
    if t > 0:
        problem += yard[t-1] + amount[t] - data['Demands'][t] == yard[t], f"Balance_Equation_{t+1}"
    else:
        problem += yard[0] == data['InitContainer'], "Initial_Containers"

    problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t], f"Cranes_Capacity_Constraint_{t+1}"
    problem += yard[t] <= data['MaxContainer'], f"Max_Container_Constraint_{t+1}"
    problem += crane[t] <= data['NumCranes'], f"Crane_Limit_Constraint_{t+1}"

#### Final constraint for yard at the last month
problem += yard[data['T']] == 0, "Final_Yard_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

