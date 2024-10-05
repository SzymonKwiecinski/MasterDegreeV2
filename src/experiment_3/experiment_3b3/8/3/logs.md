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

\section*{Mathematical Model}

Let:
\begin{itemize}
    \item $T$: Number of years
    \item $demand_t$: Demand for electricity in year $t$ (in megawatts)
    \item $oil_t$: Existing oil capacity available in year $t$ (in megawatts)
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants (in years)
    \item $nuke\_life$: Lifespan of nuclear plants (in years)
\end{itemize}

Define the decision variables:
\begin{itemize}
    \item $coal_t$: Amount of coal capacity added in year $t$
    \item $nuke_t$: Amount of nuclear capacity added in year $t$
\end{itemize}

The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^T (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\]

Subject to the following constraints:

1. **Demand Satisfaction**:
   \[
   oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j+1} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j+1} \geq demand_t \quad \forall t = 1, \ldots, T
   \]

2. **Nuclear Capacity Constraint**:
   \[
   \sum_{t=1}^{T} nuke_t \leq max\_nuke \cdot \left( \sum_{t=1}^{T} \left( oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j+1} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j+1} \right) \right) \quad \forall t = 1, \ldots, T
   \]

3. **Non-negativity**:
   \[
   coal_t \geq 0, \quad nuke_t \geq 0 \quad \forall t = 1, \ldots, T
   \]

The output will provide the following:

- "coal\_cap\_added": List of coal capacities added each year.
- "nuke\_cap\_added": List of nuclear capacities added each year.
- "total\_cost": Total cost of the capacity expansion.

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

\section*{Mathematical Model}

Let:
\begin{itemize}
    \item $T$: Number of years
    \item $demand_t$: Demand for electricity in year $t$ (in megawatts)
    \item $oil_t$: Existing oil capacity available in year $t$ (in megawatts)
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants (in years)
    \item $nuke\_life$: Lifespan of nuclear plants (in years)
\end{itemize}

Define the decision variables:
\begin{itemize}
    \item $coal_t$: Amount of coal capacity added in year $t$
    \item $nuke_t$: Amount of nuclear capacity added in year $t$
\end{itemize}

The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^T (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\]

Subject to the following constraints:

1. **Demand Satisfaction**:
   \[
   oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j+1} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j+1} \geq demand_t \quad \forall t = 1, \ldots, T
   \]

2. **Nuclear Capacity Constraint**:
   \[
   \sum_{t=1}^{T} nuke_t \leq max\_nuke \cdot \left( \sum_{t=1}^{T} \left( oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j+1} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j+1} \right) \right) \quad \forall t = 1, \ldots, T
   \]

3. **Non-negativity**:
   \[
   coal_t \geq 0, \quad nuke_t \geq 0 \quad \forall t = 1, \ldots, T
   \]

The output will provide the following:

- "coal\_cap\_added": List of coal capacities added each year.
- "nuke\_cap\_added": List of nuclear capacities added each year.
- "total\_cost": Total cost of the capacity expansion.

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 0.2,  #### Converted to fraction
    'CoalLife': 5,
    'NukeLife': 10
}

#### Initialize problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision variables
coal = [pulp.LpVariable(f'coal_{t}', lowBound=0) for t in range(data['T'])]
nuke = [pulp.LpVariable(f'nuke_{t}', lowBound=0) for t in range(data['T'])]

#### Objective function: Minimize total cost
total_cost = pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(data['T']))
problem += total_cost

#### Constraints

#### Demand satisfaction constraints
for t in range(data['T']):
    coal_capacity = pulp.lpSum(coal[max(0, t-j)] for j in range(min(t+1, data['CoalLife'])))
    nuke_capacity = pulp.lpSum(nuke[max(0, t-j)] for j in range(min(t+1, data['NukeLife'])))
    problem += data['OilCap'][t] + coal_capacity + nuke_capacity >= data['Demand'][t]

#### Nuclear capacity constraint
total_coal_nuke_capacity = pulp.lpSum(data['OilCap'][t] + pulp.lpSum(coal[max(0, t-j)] for j in range(min(t+1, data['CoalLife']))) + pulp.lpSum(nuke[max(0, t-j)] for j in range(min(t+1, data['NukeLife']))) for t in range(data['T']))
problem += pulp.lpSum(nuke[t] for t in range(data['T'])) <= data['MaxNuke'] * total_coal_nuke_capacity

#### Solve the problem
problem.solve()

#### Output results
coal_cap_added = [coal[t].varValue for t in range(data['T'])]
nuke_cap_added = [nuke[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

print(f"coal_cap_added: {coal_cap_added}")
print(f"nuke_cap_added: {nuke_cap_added}")
print(f"total_cost (Objective Value): <OBJ>{total_cost}</OBJ>")
```


