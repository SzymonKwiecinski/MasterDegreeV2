# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A state wants to plan its electricity capacity for the next \var{T} years. 
- The state has a forecast of \var{demand_t} megawatts, presumed accurate, of the demand for electricity during year \var{t}.
- The existing capacity, which is in oil-fired plants, that will not be retired and will be available during year \var{t}, is \var{oil_t}.
- There are two alternatives for expanding electric capacity: coal­ fired or nuclear power plants.
- There is a capital cost of \var{coal_cost} per megawatt of coal-fired capacity that becomes operational at the beginning of year \var{t}.
- There is a capital cost of \var{nuke_cost} per megawatt of nuclear power capacity that becomes operational at the beginning of year \var{t}.
- For various political and safety reasons, it has been decided that no more than \var{max_nuke}% of the total capacity should ever be nuclear (\var{max_nuke} is a number between 0 and 100).
- Coal plants last for \var{coal_life} years, while nuclear plants last for \var{nuke_life} years.

INPUT FORMAT: 

{
    "demand": [demand_t for t in 1, ..., T],
    "oil_cap": [oil_t for t in 1, ..., T],
    "coal_cost": coal_cost,
    "nuke_cost": nuke_cost,
    "max_nuke": max_nuke,
    "coal_life": coal_life,
    "nuke_life": nuke_life,
}


OBJECTIVE: What is the capacity expansion plan that results in the minimum cost?


OUTPUT INFO:

- the output should represent how much coal and nuclear capacity should be added in each year, and how much the total cost is.
- the output should be a dictionary with three keys: "coal_cap_added", "nuke_cap_added", and "total_cost".
- the value of "coal_cap_added" should be a list of the coal capacity added in each year.
- the value of "nuke_cap_added" should be a list of the nuclear capacity added in each year.
- the value of "total_cost" should be a single floating point number showing the total cost of the system.


OUTPUT FORMAT:

{
    "coal_cap_added": [coal_t for t in 1, ..., T],
    "nuke_cap_added": [nuke_t for t in 1, ..., T],
    "total_cost": total_cost,
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem using linear programming, we need to define our decision variables, the objective function, and the constraints. Let's construct the Linear Programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Decision Variables}
Let:
\begin{align*}
    \text{coal\_cap\_added}_t & : \text{The coal capacity added at the beginning of year } t, \quad \forall t = 1, \ldots, T. \\
    \text{nuke\_cap\_added}_t & : \text{The nuclear capacity added at the beginning of year } t, \quad \forall t = 1, \ldots, T.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost of capacity additions:
\[
    \text{Minimize} \quad \sum_{t=1}^T \left( \text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t \right)
\]

\subsection*{Constraints}

1. **Demand Satisfaction:**
   \[
   \sum_{k=1}^{t} \text{coal\_cap\_added}_k \times \mathbb{1}(t-k < \text{coal\_life}) + \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) + \text{oil\_t} \geq \text{demand\_t}, \quad \forall t = 1, \ldots, T
   \]
   where $\mathbb{1}(\cdot)$ is the indicator function ensuring the plant is still operational.

2. **Nuclear Capacity Limit:**
   \[
   \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) \leq \frac{\text{max\_nuke}}{100} \times \left( \sum_{k=1}^{t} \text{coal\_cap\_added}_k \times \mathbb{1}(t-k < \text{coal\_life}) + \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) + \text{oil\_t} \right), \quad \forall t = 1, \ldots, T
   \]

3. **Non-negativity Constraints:**
   \[
   \text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t = 1, \ldots, T
   \]

\end{document}
```

This model describes the capacity expansion planning problem using the decision variables to determine how much coal and nuclear power capacity to add each year to meet the electricity demand while minimizing costs and adhering to policy constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Decision Variables}
Let:
\begin{align*}
    \text{coal\_cap\_added}_t & : \text{The coal capacity added at the beginning of year } t, \quad \forall t = 1, \ldots, T. \\
    \text{nuke\_cap\_added}_t & : \text{The nuclear capacity added at the beginning of year } t, \quad \forall t = 1, \ldots, T.
\end{align*}

\subsection*{Objective Function}
Minimize the total cost of capacity additions:
\[
    \text{Minimize} \quad \sum_{t=1}^T \left( \text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t \right)
\]

\subsection*{Constraints}

1. **Demand Satisfaction:**
   \[
   \sum_{k=1}^{t} \text{coal\_cap\_added}_k \times \mathbb{1}(t-k < \text{coal\_life}) + \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) + \text{oil\_t} \geq \text{demand\_t}, \quad \forall t = 1, \ldots, T
   \]
   where $\mathbb{1}(\cdot)$ is the indicator function ensuring the plant is still operational.

2. **Nuclear Capacity Limit:**
   \[
   \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) \leq \frac{\text{max\_nuke}}{100} \times \left( \sum_{k=1}^{t} \text{coal\_cap\_added}_k \times \mathbb{1}(t-k < \text{coal\_life}) + \sum_{k=1}^{t} \text{nuke\_cap\_added}_k \times \mathbb{1}(t-k < \text{nuke\_life}) + \text{oil\_t} \right), \quad \forall t = 1, \ldots, T
   \]

3. **Non-negativity Constraints:**
   \[
   \text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t = 1, \ldots, T
   \]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

#### Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

#### Decision Variables
coal_cap_added = {t: pulp.LpVariable(f'coal_cap_added_{t}', lowBound=0) for t in range(1, T+1)}
nuke_cap_added = {t: pulp.LpVariable(f'nuke_cap_added_{t}', lowBound=0) for t in range(1, T+1)}

#### Objective Function
total_cost = pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(1, T+1))
problem += total_cost

#### Constraints

#### Demand Satisfaction
for t in range(1, T+1):
    coal_capacity = pulp.lpSum(coal_cap_added[k] for k in range(max(1, t-coal_life+1), t+1))
    nuke_capacity = pulp.lpSum(nuke_cap_added[k] for k in range(max(1, t-nuke_life+1), t+1))
    
    problem += coal_capacity + nuke_capacity + oil_cap[t-1] >= demand[t-1], f"Demand_Constraint_{t}"

#### Nuclear Capacity Limit
for t in range(1, T+1):
    nuke_capacity = pulp.lpSum(nuke_cap_added[k] for k in range(max(1, t-nuke_life+1), t+1))
    total_capacity = pulp.lpSum(coal_cap_added[k] for k in range(max(1, t-coal_life+1), t+1)) + nuke_capacity + oil_cap[t-1]
    
    problem += nuke_capacity <= max_nuke / 100.0 * total_capacity, f"Nuke_Capacity_Limit_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

