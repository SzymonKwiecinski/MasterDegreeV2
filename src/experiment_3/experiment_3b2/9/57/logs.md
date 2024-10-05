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
To model the problem as a Mixed Integer Programming (MIP) problem and provide a solution in LaTeX, we need to define the decision variables, constraints, and the objective function clearly. Let's create the mathematical model in LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Seaport Container Management Model}

\subsection*{Decision Variables}
\begin{align*}
x_t &\quad \text{Number of containers unloaded in month } t, \\
y_t &\quad \text{Number of cranes rented in month } t, \\
s_t &\quad \text{Inventory of containers in the yard at the end of month } t.
\end{align*}

\subsection*{Parameters}
\begin{align*}
demand_t &\quad \text{Demand for containers by ships in month } t, \\
unload\_cost_t &\quad \text{Cost to unload a container in month } t, \\
unload\_capacity_t &\quad \text{Maximum unloading capacity in month } t, \\
holding\_cost &\quad \text{Cost to hold a container per month}, \\
max\_container &\quad \text{Maximum storage capacity of the yard}, \\
init\_container &\quad \text{Initial number of containers in the yard}, \\
num\_cranes &\quad \text{Maximum number of cranes available}, \\
crane\_capacity &\quad \text{Loading capacity of each crane}, \\
crane\_cost &\quad \text{Rental cost per crane}.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_t \cdot x_t + holding\_cost \cdot s_t + crane\_cost \cdot y_t \right)
\]

\subsection*{Constraints}
\begin{align*}
x_t &\leq unload\_capacity_t, & \forall t, \\
s_1 &= init\_container + x_1 - demand_1, \\
s_t &= s_{t-1} + x_t - demand_t, & \forall t \geq 2, \\
s_t &\leq max\_container, & \forall t, \\
y_t \cdot crane\_capacity &\geq demand_t, & \forall t, \\
y_t &\leq num\_cranes, & \forall t, \\
s_T &= 0, \\
x_t &\geq 0, & \forall t, \\
y_t &\in \mathbb{Z}_{\geq 0}, & \forall t, \\
s_t &\geq 0, & \forall t.
\end{align*}

\subsection*{Description}
This model aims to minimize the total cost of unloading, holding in the yard, and crane rentals over the planning horizon of $T$ months. The constraints ensure that:
- Unloading per month does not exceed the capacity.
- Inventory balance is maintained across months.
- The yard does not exceed its storage capacity.
- Crane rentals are sufficient to meet the loading demands.
- The yard is empty by the end of the planning horizon.
- Variables are non-negative, and crane rentals are integer.

\end{document}
```

The above LaTeX code models the seaport container management problem as a Mixed Integer Programming problem. The decision variables `x_t`, `y_t`, and `s_t` are used to determine the number of containers unloaded, cranes rented, and inventory held each month, respectively. The objective is to minimize the costs associated with these activities over the period. The constraints ensure operational feasibility for unloading, storage, and loading activities.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Seaport Container Management Model}

\subsection*{Decision Variables}
\begin{align*}
x_t &\quad \text{Number of containers unloaded in month } t, \\
y_t &\quad \text{Number of cranes rented in month } t, \\
s_t &\quad \text{Inventory of containers in the yard at the end of month } t.
\end{align*}

\subsection*{Parameters}
\begin{align*}
demand_t &\quad \text{Demand for containers by ships in month } t, \\
unload\_cost_t &\quad \text{Cost to unload a container in month } t, \\
unload\_capacity_t &\quad \text{Maximum unloading capacity in month } t, \\
holding\_cost &\quad \text{Cost to hold a container per month}, \\
max\_container &\quad \text{Maximum storage capacity of the yard}, \\
init\_container &\quad \text{Initial number of containers in the yard}, \\
num\_cranes &\quad \text{Maximum number of cranes available}, \\
crane\_capacity &\quad \text{Loading capacity of each crane}, \\
crane\_cost &\quad \text{Rental cost per crane}.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \left( unload\_cost_t \cdot x_t + holding\_cost \cdot s_t + crane\_cost \cdot y_t \right)
\]

\subsection*{Constraints}
\begin{align*}
x_t &\leq unload\_capacity_t, & \forall t, \\
s_1 &= init\_container + x_1 - demand_1, \\
s_t &= s_{t-1} + x_t - demand_t, & \forall t \geq 2, \\
s_t &\leq max\_container, & \forall t, \\
y_t \cdot crane\_capacity &\geq demand_t, & \forall t, \\
y_t &\leq num\_cranes, & \forall t, \\
s_T &= 0, \\
x_t &\geq 0, & \forall t, \\
y_t &\in \mathbb{Z}_{\geq 0}, & \forall t, \\
s_t &\geq 0, & \forall t.
\end{align*}

\subsection*{Description}
This model aims to minimize the total cost of unloading, holding in the yard, and crane rentals over the planning horizon of $T$ months. The constraints ensure that:
- Unloading per month does not exceed the capacity.
- Inventory balance is maintained across months.
- The yard does not exceed its storage capacity.
- Crane rentals are sufficient to meet the loading demands.
- The yard is empty by the end of the planning horizon.
- Variables are non-negative, and crane rentals are integer.

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

#### Initialize the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("unloaded", range(1, data['T'] + 1), lowBound=0, upBound=None)  #### Number of containers unloaded
y = pulp.LpVariable.dicts("cranes", range(1, data['T'] + 1), lowBound=0, cat='Integer')  #### Number of cranes rented
s = pulp.LpVariable.dicts("inventory", range(1, data['T'] + 1), lowBound=0)  #### Inventory at the end of each month

#### Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(1, data['T'] + 1))

#### Constraints
for t in range(1, data['T'] + 1):
    problem += x[t] <= data['UnloadCapacity'][t-1], f"Unload_Capacity_Constraint_{t}"

problem += s[1] == data['InitContainer'] + x[1] - data['Demands'][0], "Initial_Inventory_Constraint"

for t in range(2, data['T'] + 1):
    problem += s[t] == s[t-1] + x[t] - data['Demands'][t-1], f"Inventory_Balance_Constraint_{t}"

for t in range(1, data['T'] + 1):
    problem += s[t] <= data['MaxContainer'], f"Max_Container_Constraint_{t}"
    problem += y[t] * data['CraneCapacity'] >= data['Demands'][t-1], f"Cranes_Capacity_Constraint_{t}"
    problem += y[t] <= data['NumCranes'], f"Max_Cranes_Constraint_{t}"

problem += s[data['T']] == 0, "Final_Inventory_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

