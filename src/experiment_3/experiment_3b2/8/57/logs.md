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
To construct a mathematical model for the given problem, we need to define the decision variables, constraints, and the objective function.

Let's define the decision variables:
- \( x_t \): Number of containers unloaded in month \( t \)
- \( y_t \): Number of cranes rented in month \( t \)
- \( s_t \): Number of containers stored in the yard at the end of month \( t \)

We aim to minimize the total cost, which includes the unloading cost, holding cost, and crane rental cost, over the period. Now, let's write the mathematical formulation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_t \cdot x_t + \text{holding\_cost} \cdot s_t + \text{crane\_cost} \cdot y_t \right)
\]

\textbf{Constraints:}
\begin{align*}
\text{(1) Load containers to satisfy demand:} &\\
& x_t + s_{t-1} = \text{demand}_t + s_t, & \forall t \in \{1, \dots, T\}\\
\text{(2) Initial containers in yard:} &\\
& s_0 = \text{init\_container}\\
\text{(3) Final yard condition:} &\\
& s_T = 0\\
\text{(4) Unloading capacity constraint:} &\\
& x_t \leq \text{unload\_capacity}_t, & \forall t \in \{1, \dots, T\}\\
\text{(5) Maximum yard capacity constraint:} &\\
& s_t \leq \text{max\_container}, & \forall t \in \{1, \dots, T\}\\
\text{(6) Crane capacity constraint:} &\\
& \text{demand}_t \leq \text{crane\_capacity} \cdot y_t, & \forall t \in \{1, \dots, T\}\\
\text{(7) Maximum number of cranes constraint:} &\\
& y_t \leq \text{num\_cranes}, & \forall t \in \{1, \dots, T\}\\
\text{(8) Non-negativity constraints:} &\\
& x_t, s_t, y_t \geq 0, & \forall t \in \{1, \dots, T\} \\
& x_t, s_t, y_t \text{ are integers}, & \forall t \in \{1, \dots, T\}
\end{align*}

\end{document}
```

In this model:
- The objective function minimizes the sum of unloading costs, holding costs, and crane rental costs.
- Constraint (1) ensures that the total containers (unloaded + stored) meet the demand while accounting for storage.
- Constraint (2) specifies the initial condition for storage.
- Constraint (3) enforces that no containers remain in storage at the end of the planning horizon.
- Constraint (4) ensures that the number of containers unloaded does not exceed the unloading capacity.
- Constraint (5) maintains the maximum storage limitation.
- Constraint (6) matches the demand with available crane capacity.
- Constraint (7) limits the number of cranes rented each month.
- Constraint (8) ensures non-negativity and integrality of decision variables.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:}
\[
\min \sum_{t=1}^{T} \left( \text{unload\_cost}_t \cdot x_t + \text{holding\_cost} \cdot s_t + \text{crane\_cost} \cdot y_t \right)
\]

\textbf{Constraints:}
\begin{align*}
\text{(1) Load containers to satisfy demand:} &\\
& x_t + s_{t-1} = \text{demand}_t + s_t, & \forall t \in \{1, \dots, T\}\\
\text{(2) Initial containers in yard:} &\\
& s_0 = \text{init\_container}\\
\text{(3) Final yard condition:} &\\
& s_T = 0\\
\text{(4) Unloading capacity constraint:} &\\
& x_t \leq \text{unload\_capacity}_t, & \forall t \in \{1, \dots, T\}\\
\text{(5) Maximum yard capacity constraint:} &\\
& s_t \leq \text{max\_container}, & \forall t \in \{1, \dots, T\}\\
\text{(6) Crane capacity constraint:} &\\
& \text{demand}_t \leq \text{crane\_capacity} \cdot y_t, & \forall t \in \{1, \dots, T\}\\
\text{(7) Maximum number of cranes constraint:} &\\
& y_t \leq \text{num\_cranes}, & \forall t \in \{1, \dots, T\}\\
\text{(8) Non-negativity constraints:} &\\
& x_t, s_t, y_t \geq 0, & \forall t \in \{1, \dots, T\} \\
& x_t, s_t, y_t \text{ are integers}, & \forall t \in \{1, \dots, T\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

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

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Unload", range(1, data['T'] + 1), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("Storage", range(0, data['T'] + 1), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Cranes", range(1, data['T'] + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')

#### Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(1, data['T'] + 1))

#### Constraints
#### (1) Load containers to satisfy demand
for t in range(1, data['T'] + 1):
    if t == 1:
        problem += x[t] + data['InitContainer'] == data['Demands'][t-1] + s[t]
    else:
        problem += x[t] + s[t-1] == data['Demands'][t-1] + s[t]

#### (2) Final yard condition
problem += s[data['T']] == 0

#### (3) Unloading capacity constraint
for t in range(1, data['T'] + 1):
    problem += x[t] <= data['UnloadCapacity'][t-1]

#### (4) Maximum yard capacity constraint
for t in range(1, data['T'] + 1):
    problem += s[t] <= data['MaxContainer']

#### (5) Crane capacity constraint
for t in range(1, data['T'] + 1):
    problem += data['Demands'][t-1] <= data['CraneCapacity'] * y[t]

#### (6) Maximum number of cranes constraint
for t in range(1, data['T'] + 1):
    problem += y[t] <= data['NumCranes']

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

