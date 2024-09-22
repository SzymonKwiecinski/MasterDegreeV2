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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{align*}
T & : \text{number of years} \\
demand_t & : \text{megawatts of electricity demand in year } t \\
oil_t & : \text{existing oil-fired capacity in year } t \\
coal\_cost & : \text{capital cost per megawatt of coal-fired capacity} \\
nuke\_cost & : \text{capital cost per megawatt of nuclear power capacity} \\
max\_nuke & : \text{maximum allowable percentage of nuclear capacity} \\
coal\_life & : \text{lifetime of coal plants in years} \\
nuke\_life & : \text{lifetime of nuclear plants in years} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
coal_t & : \text{amount of coal-fired capacity added in year } t \\
nuke_t & : \text{amount of nuclear capacity added in year } t \\
\end{align*}

\subsection*{Objective Function}
Minimize the total cost of capacity expansion:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \left( coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t \right)
\]

\subsection*{Constraints}
1. **Capacity Constraint**:
   The total capacity available in year \( t \) must meet the demand:
   \[
   oil_t + \sum_{j=0}^{\min(t-1, coal\_life-1)} coal_{t-j} + \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \geq demand_t \quad \forall t \in \{1, \ldots, T\}
   \]

2. **Nuclear Capacity Limit**:
   The nuclear capacity must not exceed the specified percentage of total capacity:
   \[
   \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \leq \frac{max\_nuke}{100} \left( oil_t + \sum_{j=0}^{\min(t-1, coal\_life-1)} coal_{t-j} + \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \right) \quad \forall t \in \{1, \ldots, T\}
   \]

3. **Non-negativity Constraints**:
   The capacities added must be non-negative:
   \[
   coal_t \geq 0, \quad nuke_t \geq 0 \quad \forall t \in \{1, \ldots, T\}
   \]

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

\section*{Mathematical Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{align*}
T & : \text{number of years} \\
demand_t & : \text{megawatts of electricity demand in year } t \\
oil_t & : \text{existing oil-fired capacity in year } t \\
coal\_cost & : \text{capital cost per megawatt of coal-fired capacity} \\
nuke\_cost & : \text{capital cost per megawatt of nuclear power capacity} \\
max\_nuke & : \text{maximum allowable percentage of nuclear capacity} \\
coal\_life & : \text{lifetime of coal plants in years} \\
nuke\_life & : \text{lifetime of nuclear plants in years} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
coal_t & : \text{amount of coal-fired capacity added in year } t \\
nuke_t & : \text{amount of nuclear capacity added in year } t \\
\end{align*}

\subsection*{Objective Function}
Minimize the total cost of capacity expansion:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \left( coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t \right)
\]

\subsection*{Constraints}
1. **Capacity Constraint**:
   The total capacity available in year \( t \) must meet the demand:
   \[
   oil_t + \sum_{j=0}^{\min(t-1, coal\_life-1)} coal_{t-j} + \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \geq demand_t \quad \forall t \in \{1, \ldots, T\}
   \]

2. **Nuclear Capacity Limit**:
   The nuclear capacity must not exceed the specified percentage of total capacity:
   \[
   \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \leq \frac{max\_nuke}{100} \left( oil_t + \sum_{j=0}^{\min(t-1, coal\_life-1)} coal_{t-j} + \sum_{k=0}^{\min(t-1, nuke\_life-1)} nuke_{t-k} \right) \quad \forall t \in \{1, \ldots, T\}
   \]

3. **Non-negativity Constraints**:
   The capacities added must be non-negative:
   \[
   coal_t \geq 0, \quad nuke_t \geq 0 \quad \forall t \in \{1, \ldots, T\}
   \]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Problem
problem = pulp.LpProblem("Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_vars = pulp.LpVariable.dicts("coal", (t for t in range(T)), lowBound=0, cat=pulp.LpContinuous)
nuke_vars = pulp.LpVariable.dicts("nuke", (t for t in range(T)), lowBound=0, cat=pulp.LpContinuous)

#### Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(T)), "Total Cost"

#### Constraints

#### Capacity Constraint
for t in range(T):
    coal_sum = pulp.lpSum(coal_vars[t - j] for j in range(min(t, coal_life)))
    nuke_sum = pulp.lpSum(nuke_vars[t - k] for k in range(min(t, nuke_life)))
    problem += oil_cap[t] + coal_sum + nuke_sum >= demand[t], f"DemandConstraint_{t}"

#### Nuclear Capacity Limit
for t in range(T):
    nuke_sum = pulp.lpSum(nuke_vars[t - k] for k in range(min(t, nuke_life)))
    coal_sum = pulp.lpSum(coal_vars[t - j] for j in range(min(t, coal_life)))
    problem += nuke_sum <= max_nuke * (oil_cap[t] + coal_sum + nuke_sum), f"NukeLimit_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

