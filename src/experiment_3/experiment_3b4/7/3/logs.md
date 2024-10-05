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
To model the given problem as a Linear Programming problem, we need to define decision variables, constraints, and the objective function that minimizes the total cost of expanding the electricity capacity.

######### Decision Variables

1. \( \text{coal\_cap\_added}_t \): The amount of coal-fired capacity added in year \( t \).
2. \( \text{nuke\_cap\_added}_t \): The amount of nuclear capacity added in year \( t \).

######### Parameters

- \( \text{demand}_t \): Forecasted demand for electricity in year \( t \).
- \( \text{oil\_cap}_t \): Existing oil-fired capacity available in year \( t \).
- \( \text{coal\_cost} \): Capital cost per megawatt of coal-fired capacity.
- \( \text{nuke\_cost} \): Capital cost per megawatt of nuclear power capacity.
- \( \text{max\_nuke} \): Maximum percentage of total capacity that can be nuclear.
- \( \text{coal\_life} \): Lifetime of coal plants in years.
- \( \text{nuke\_life} \): Lifetime of nuclear plants in years.

######### Objective Function

Minimize the total cost of adding capacity over \( T \) years:

\[
\text{Minimize} \quad \sum_{t=1}^{T} (\text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t)
\]

######### Constraints

1. **Demand Satisfaction**: Total capacity (existing and added) must meet or exceed demand each year.

\[
\text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \geq \text{demand}_t, \quad \forall t
\]

2. **Nuclear Capacity Limit**: The nuclear capacity should not exceed the specified percentage of total capacity.

\[
\sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \leq \frac{\text{max\_nuke}}{100} \left( \text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \right), \quad \forall t
\]

3. **Non-negativity**: The capacities added must be non-negative.

\[
\text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t
\]

Below is the complete LATEX representation of the linear programming model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{t=1}^{T} (\text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t)
\]

\subsection*{Constraints}

\paragraph{Demand Satisfaction:}
\[
\text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \geq \text{demand}_t, \quad \forall t
\]

\paragraph{Nuclear Capacity Limit:}
\[
\sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \leq \frac{\text{max\_nuke}}{100} \left( \text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \right), \quad \forall t
\]

\paragraph{Non-negativity:}
\[
\text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t
\]

\end{document}
```

This model will help determine the optimal plan for capacity expansion in terms of minimizing costs while satisfying demand and regulatory limitations for nuclear capacity.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Objective Function}
\[
\text{Minimize} \quad \sum_{t=1}^{T} (\text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t)
\]

\subsection*{Constraints}

\paragraph{Demand Satisfaction:}
\[
\text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \geq \text{demand}_t, \quad \forall t
\]

\paragraph{Nuclear Capacity Limit:}
\[
\sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \leq \frac{\text{max\_nuke}}{100} \left( \text{oil\_cap}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_cap\_added}_i + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_cap\_added}_i \right), \quad \forall t
\]

\paragraph{Non-negativity:}
\[
\text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
T = 12
Demand = [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35]
OilCap = [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5]
CoalCost = 10
NukeCost = 5
MaxNuke = 20
CoalLife = 5
NukeLife = 10

#### Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_cap_added = [pulp.LpVariable(f"coal_cap_added_{t}", lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f"nuke_cap_added_{t}", lowBound=0) for t in range(T)]

#### Objective Function
problem += pulp.lpSum(CoalCost * coal_cap_added[t] + NukeCost * nuke_cap_added[t] for t in range(T)), "Total Cost"

#### Constraints

#### Demand Satisfaction
for t in range(T):
    coal_life_sum = pulp.lpSum(coal_cap_added[i] for i in range(max(0, t-CoalLife+1), t+1))
    nuke_life_sum = pulp.lpSum(nuke_cap_added[i] for i in range(max(0, t-NukeLife+1), t+1))
    problem += OilCap[t] + coal_life_sum + nuke_life_sum >= Demand[t], f"Demand_Satisfaction_{t}"

#### Nuclear Capacity Limit
for t in range(T):
    nuke_life_sum = pulp.lpSum(nuke_cap_added[i] for i in range(max(0, t-NukeLife+1), t+1))
    total_capacity = OilCap[t] + pulp.lpSum(coal_cap_added[i] for i in range(max(0, t-CoalLife+1), t+1)) + nuke_life_sum
    problem += nuke_life_sum <= MaxNuke / 100 * total_capacity, f"Nuclear_Capacity_Limit_{t}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

