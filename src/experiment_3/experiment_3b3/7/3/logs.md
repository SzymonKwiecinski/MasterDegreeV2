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

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{align*}
T & \quad \text{(number of years)} \\
demand_t & \quad \text{(demand for electricity in year } t \text{)} \\
oil_t & \quad \text{(existing oil-fired capacity in year } t \text{)} \\
coal\_cost & \quad \text{(cost per megawatt of coal-fired capacity)} \\
nuke\_cost & \quad \text{(cost per megawatt of nuclear capacity)} \\
max\_nuke & \quad \text{(maximum percentage of total capacity that can be nuclear)} \\
coal\_life & \quad \text{(lifetime of coal plants in years)} \\
nuke\_life & \quad \text{(lifetime of nuclear plants in years)} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{coal\_added}_t & \quad \text{(coal capacity added in year } t\text{)} \\
\text{nuke\_added}_t & \quad \text{(nuclear capacity added in year } t\text{)} \\
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Minimize } Z & = \sum_{t=1}^{T} (coal\_cost \cdot coal\_added_t + nuke\_cost \cdot nuke\_added_t)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{t'=t}^{\min(t + coal\_life - 1, T)} coal\_added_{t'} & \quad \text{(total coal capacity)} \\
\sum_{t'=t}^{\min(t + nuke\_life - 1, T)} nuke\_added_{t'} & \quad \text{(total nuclear capacity)} \\
oil_t + \sum_{t'=1}^{t} coal\_added_{t'} + \sum_{t'=1}^{t} nuke\_added_{t'} & \geq demand_t \quad \forall t \\
\sum_{t'=1}^{T} nuke\_added_{t'} & \leq \frac{max\_nuke}{100} \cdot \left( \sum_{t'=1}^{T} oil_t + \sum_{t'=1}^{T} coal\_added_{t'} + \sum_{t'=1}^{T} nuke\_added_{t'} \right) \\
\end{align*}

\subsection*{Output}
The solution will provide:
\begin{align*}
\text{coal\_cap\_added} & \quad \text{(list of coal capacity added each year)} \\
\text{nuke\_cap\_added} & \quad \text{(list of nuclear capacity added each year)} \\
\text{total\_cost} & \quad \text{(total cost of the system)}
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

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{align*}
T & \quad \text{(number of years)} \\
demand_t & \quad \text{(demand for electricity in year } t \text{)} \\
oil_t & \quad \text{(existing oil-fired capacity in year } t \text{)} \\
coal\_cost & \quad \text{(cost per megawatt of coal-fired capacity)} \\
nuke\_cost & \quad \text{(cost per megawatt of nuclear capacity)} \\
max\_nuke & \quad \text{(maximum percentage of total capacity that can be nuclear)} \\
coal\_life & \quad \text{(lifetime of coal plants in years)} \\
nuke\_life & \quad \text{(lifetime of nuclear plants in years)} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{coal\_added}_t & \quad \text{(coal capacity added in year } t\text{)} \\
\text{nuke\_added}_t & \quad \text{(nuclear capacity added in year } t\text{)} \\
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Minimize } Z & = \sum_{t=1}^{T} (coal\_cost \cdot coal\_added_t + nuke\_cost \cdot nuke\_added_t)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\sum_{t'=t}^{\min(t + coal\_life - 1, T)} coal\_added_{t'} & \quad \text{(total coal capacity)} \\
\sum_{t'=t}^{\min(t + nuke\_life - 1, T)} nuke\_added_{t'} & \quad \text{(total nuclear capacity)} \\
oil_t + \sum_{t'=1}^{t} coal\_added_{t'} + \sum_{t'=1}^{t} nuke\_added_{t'} & \geq demand_t \quad \forall t \\
\sum_{t'=1}^{T} nuke\_added_{t'} & \leq \frac{max\_nuke}{100} \cdot \left( \sum_{t'=1}^{T} oil_t + \sum_{t'=1}^{T} coal\_added_{t'} + \sum_{t'=1}^{T} nuke\_added_{t'} \right) \\
\end{align*}

\subsection*{Output}
The solution will provide:
\begin{align*}
\text{coal\_cap\_added} & \quad \text{(list of coal capacity added each year)} \\
\text{nuke\_cap\_added} & \quad \text{(list of nuclear capacity added each year)} \\
\text{total\_cost} & \quad \text{(total cost of the system)}
\end{align*}

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

#### Extracting data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_added = pulp.LpVariable.dicts("Coal_Added", range(T), lowBound=0)
nuke_added = pulp.LpVariable.dicts("Nuke_Added", range(T), lowBound=0)

#### Objective Function
problem += pulp.lpSum(coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T)), "Total Cost"

#### Constraints

#### Demand constraints
for t in range(T):
    problem += (
        oil_cap[t] + pulp.lpSum(coal_added[t_] for t_ in range(t+1)) + pulp.lpSum(nuke_added[t_] for t_ in range(t+1)) 
        >= demand[t], 
        f"Demand_Constraint_{t}"
    )

#### Nuclear capacity percentage constraint
problem += (
    pulp.lpSum(nuke_added[t] for t in range(T)) 
    <= (max_nuke / 100) * (pulp.lpSum(oil_cap[t] for t in range(T)) + pulp.lpSum(coal_added[t] for t in range(T)) + pulp.lpSum(nuke_added[t] for t in range(T))), 
    "Max_Nuclear_Capacity_Constraint"
)

#### Solve the problem
problem.solve()

#### Extracting results
coal_cap_added = [coal_added[t].varValue for t in range(T)]
nuke_cap_added = [nuke_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

#### Print outputs
print("Coal Capacity Added Each Year:", coal_cap_added)
print("Nuclear Capacity Added Each Year:", nuke_cap_added)
print("Total Cost:", total_cost)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

