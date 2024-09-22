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
To create a linear programming model for the given problem, we need to define variables, constraints, and the objective function in the context of the problem's requirements and inputs.

Let's define the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Electricity Capacity Expansion Model}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Total number of years for planning.
    \item $demand_t$: Forecasted electricity demand in megawatts for year $t$.
    \item $oil_t$: Existing oil-fired capacity available in year $t$.
    \item $coal\_cost$: Capital cost per megawatt for coal-fired capacity.
    \item $nuke\_cost$: Capital cost per megawatt for nuclear capacity.
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear.
    \item $coal\_life$: Lifespan of coal plants in years.
    \item $nuke\_life$: Lifespan of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{coal}$: Megawatts of coal capacity added in year $t$.
    \item $x_t^{nuke}$: Megawatts of nuclear capacity added in year $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{t=1}^{T} (coal\_cost \times x_t^{coal} + nuke\_cost \times x_t^{nuke})
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:} For each year $t$, the total available capacity should meet or exceed the demand.
    \[
    oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{coal} + \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Nuclear Capacity Limit:} The total nuclear capacity should not exceed the maximum allowed percentage of total capacity.
    \[
    \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \leq max\_nuke \times \left( oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{coal} + \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \right) / 100, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Non-negativity:} The added capacities must be non-negative.
    \[
    x_t^{coal} \geq 0, \quad x_t^{nuke} \geq 0, \quad \forall t = 1, \ldots, T
    \]
\end{itemize}

\end{document}
```

This linear programming model aims to minimize the total capital cost required to meet the demand for electricity while adhering to constraints about the lifespan of plants and the proportion of nuclear energy.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Electricity Capacity Expansion Model}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Total number of years for planning.
    \item $demand_t$: Forecasted electricity demand in megawatts for year $t$.
    \item $oil_t$: Existing oil-fired capacity available in year $t$.
    \item $coal\_cost$: Capital cost per megawatt for coal-fired capacity.
    \item $nuke\_cost$: Capital cost per megawatt for nuclear capacity.
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear.
    \item $coal\_life$: Lifespan of coal plants in years.
    \item $nuke\_life$: Lifespan of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{coal}$: Megawatts of coal capacity added in year $t$.
    \item $x_t^{nuke}$: Megawatts of nuclear capacity added in year $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{t=1}^{T} (coal\_cost \times x_t^{coal} + nuke\_cost \times x_t^{nuke})
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:} For each year $t$, the total available capacity should meet or exceed the demand.
    \[
    oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{coal} + \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Nuclear Capacity Limit:} The total nuclear capacity should not exceed the maximum allowed percentage of total capacity.
    \[
    \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \leq max\_nuke \times \left( oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{coal} + \sum_{k=\max(1, t-nuke\_life+1)}^{t} x_k^{nuke} \right) / 100, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Non-negativity:} The added capacities must be non-negative.
    \[
    x_t^{coal} \geq 0, \quad x_t^{nuke} \geq 0, \quad \forall t = 1, \ldots, T
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision variables
x_coal = {t: pulp.LpVariable(f"x_coal_{t}", lowBound=0, cat='Continuous') for t in range(1, T+1)}
x_nuke = {t: pulp.LpVariable(f"x_nuke_{t}", lowBound=0, cat='Continuous') for t in range(1, T+1)}

#### Objective function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(1, T+1))

#### Constraints
for t in range(1, T+1):
    coal_cap_t = pulp.lpSum(x_coal[j] for j in range(max(1, t-coal_life+1), t+1))
    nuke_cap_t = pulp.lpSum(x_nuke[k] for k in range(max(1, t-nuke_life+1), t+1))
    
    #### Demand satisfaction
    problem += oil_cap[t-1] + coal_cap_t + nuke_cap_t >= demand[t-1]
    
    #### Nuclear capacity limit
    problem += nuke_cap_t <= max_nuke * (oil_cap[t-1] + coal_cap_t + nuke_cap_t) / 100

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

