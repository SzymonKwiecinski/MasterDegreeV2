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
\begin{itemize}
    \item $T$: Total number of years
    \item $demand_t$: Demand for electricity in year $t$ (in megawatts)
    \item $oil_t$: Existing oil-fired capacity in year $t$ (in megawatts)
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants (in years)
    \item $nuke\_life$: Lifespan of nuclear plants (in years)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $coal_t$: Amount of coal capacity added in year $t$ (in megawatts)
    \item $nuke_t$: Amount of nuclear capacity added in year $t$ (in megawatts)
\end{itemize}

\subsection*{Objective Function}
\begin{align*}
    \text{Minimize} \quad Z = \sum_{t=1}^{T} (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    \text{Capacity Constraint:} \quad \sum_{j=\max(1, t - coal\_life + 1)}^{t} coal_j + \sum_{j=\max(1, t - nuke\_life + 1)}^{t} nuke_j + oil_t \geq demand_t & \quad \forall t = 1, \ldots, T \\
    \text{Nuclear Capacity Constraint:} \quad \sum_{j=1}^{t} nuke_j \leq \frac{max\_nuke}{100} \left( \sum_{j=1}^{t} (coal_j + nuke_j + oil_t) \right) & \quad \forall t = 1, \ldots, T \\
    \text{Non-negativity Constraint:} \quad coal_t \geq 0, \, nuke_t \geq 0 & \quad \forall t = 1, \ldots, T
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

\section*{Mathematical Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Total number of years
    \item $demand_t$: Demand for electricity in year $t$ (in megawatts)
    \item $oil_t$: Existing oil-fired capacity in year $t$ (in megawatts)
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants (in years)
    \item $nuke\_life$: Lifespan of nuclear plants (in years)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $coal_t$: Amount of coal capacity added in year $t$ (in megawatts)
    \item $nuke_t$: Amount of nuclear capacity added in year $t$ (in megawatts)
\end{itemize}

\subsection*{Objective Function}
\begin{align*}
    \text{Minimize} \quad Z = \sum_{t=1}^{T} (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\end{align*}

\subsection*{Constraints}
\begin{align*}
    \text{Capacity Constraint:} \quad \sum_{j=\max(1, t - coal\_life + 1)}^{t} coal_j + \sum_{j=\max(1, t - nuke\_life + 1)}^{t} nuke_j + oil_t \geq demand_t & \quad \forall t = 1, \ldots, T \\
    \text{Nuclear Capacity Constraint:} \quad \sum_{j=1}^{t} nuke_j \leq \frac{max\_nuke}{100} \left( \sum_{j=1}^{t} (coal_j + nuke_j + oil_t) \right) & \quad \forall t = 1, \ldots, T \\
    \text{Non-negativity Constraint:} \quad coal_t \geq 0, \, nuke_t \geq 0 & \quad \forall t = 1, \ldots, T
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
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

#### Model initialization
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal = pulp.LpVariable.dicts("coal", range(1, data['T'] + 1), lowBound=0)
nuke = pulp.LpVariable.dicts("nuke", range(1, data['T'] + 1), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(1, data['T'] + 1))

#### Constraints
for t in range(1, data['T'] + 1):
    #### Capacity Constraint
    problem += (
        pulp.lpSum(coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
        data['OilCap'][t - 1] >= data['Demand'][t - 1],
        f"Capacity_Constraint_{t}"
    )
    
    #### Nuclear Capacity Constraint
    problem += (
        pulp.lpSum(nuke[j] for j in range(1, t + 1)) <= 
        (data['MaxNuke'] / 100) * pulp.lpSum(coal[j] + nuke[j] + data['OilCap'][t - 1] for j in range(1, t + 1)),
        f"Nuclear_Capacity_Constraint_{t}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

