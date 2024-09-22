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
    \item $demand_t$: Demand for electricity in year $t$, for $t = 1, \ldots, T$
    \item $oil_t$: Existing oil-fired capacity in year $t$, for $t = 1, \ldots, T$
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants in years
    \item $nuke\_life$: Lifespan of nuclear plants in years
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $coal_t$: Coal capacity added in year $t$, for $t = 1, \ldots, T$
    \item $nuke_t$: Nuclear capacity added in year $t$, for $t = 1, \ldots, T$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } \sum_{t=1}^{T} \left( coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t \right)
\]

\subsection*{Constraints}
1. Total capacity must meet demand:
\[
oil_t + \sum_{s=1}^{\min(t, coal\_life)} coal_{t-s} + \sum_{s=1}^{\min(t, nuke\_life)} nuke_{t-s} \geq demand_t, \quad \forall t \in \{1, \ldots, T\}
\]

2. Nuclear capacity constraint:
\[
\frac{\sum_{s=1}^{T} nuke_s}{\sum_{s=1}^{T} coal_s + \sum_{s=1}^{T} nuke_s + \sum_{s=1}^{T} oil_s} \leq \frac{max\_nuke}{100}
\]

3. Non-negativity constraints:
\[
coal_t \geq 0, \quad nuke_t \geq 0, \quad \forall t \in \{1, \ldots, T\}
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
\begin{itemize}
    \item $T$: Total number of years
    \item $demand_t$: Demand for electricity in year $t$, for $t = 1, \ldots, T$
    \item $oil_t$: Existing oil-fired capacity in year $t$, for $t = 1, \ldots, T$
    \item $coal\_cost$: Capital cost per megawatt of coal-fired capacity
    \item $nuke\_cost$: Capital cost per megawatt of nuclear power capacity
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear
    \item $coal\_life$: Lifespan of coal plants in years
    \item $nuke\_life$: Lifespan of nuclear plants in years
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $coal_t$: Coal capacity added in year $t$, for $t = 1, \ldots, T$
    \item $nuke_t$: Nuclear capacity added in year $t$, for $t = 1, \ldots, T$
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } \sum_{t=1}^{T} \left( coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t \right)
\]

\subsection*{Constraints}
1. Total capacity must meet demand:
\[
oil_t + \sum_{s=1}^{\min(t, coal\_life)} coal_{t-s} + \sum_{s=1}^{\min(t, nuke\_life)} nuke_{t-s} \geq demand_t, \quad \forall t \in \{1, \ldots, T\}
\]

2. Nuclear capacity constraint:
\[
\frac{\sum_{s=1}^{T} nuke_s}{\sum_{s=1}^{T} coal_s + \sum_{s=1}^{T} nuke_s + \sum_{s=1}^{T} oil_s} \leq \frac{max\_nuke}{100}
\]

3. Non-negativity constraints:
\[
coal_t \geq 0, \quad nuke_t \geq 0, \quad \forall t \in \{1, \ldots, T\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

#### Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal = pulp.LpVariable.dicts("Coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("Nuke", range(1, T + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(1, T + 1)), "Total Cost"

#### Constraints
for t in range(1, T + 1):
    problem += (oil_capacity[t-1] + 
                pulp.lpSum(coal[t-s] for s in range(1, min(t, coal_life) + 1)) + 
                pulp.lpSum(nuke[t-s] for s in range(1, min(t, nuke_life) + 1)) >= demand[t-1]), f"Demand_Constraint_{t}")

#### Nuclear capacity constraint
problem += (pulp.lpSum(nuke[s] for s in range(1, T + 1)) / 
            (pulp.lpSum(coal[s] for s in range(1, T + 1)) + 
             pulp.lpSum(nuke[s] for s in range(1, T + 1)) + 
             pulp.lpSum(oil_capacity[s-1] for s in range(1, T + 1))) <= max_nuke / 100), "Nuclear_Capacity_Constraint")

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


