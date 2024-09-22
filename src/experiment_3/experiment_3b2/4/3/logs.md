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
To formulate the given problem as a Linear Programming (LP) model, we need to define decision variables, the objective function, and the constraints based on the problem description. Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of years for planning.
    \item $\text{demand}_t$: Demand for electricity in megawatts in year $t$, for $t = 1, \ldots, T$.
    \item $\text{oil}_t$: Existing oil-fired capacity available in year $t$, for $t = 1, \ldots, T$.
    \item $\text{coal\_cost}$: Capital cost per megawatt for coal-fired capacity.
    \item $\text{nuke\_cost}$: Capital cost per megawatt for nuclear power capacity.
    \item $\text{max\_nuke}$: Maximum percentage of total capacity that can be nuclear.
    \item $\text{coal\_life}$: Lifespan of coal plants in years.
    \item $\text{nuke\_life}$: Lifespan of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{coal}$: New coal-fired capacity added in year $t$, for $t = 1, \ldots, T$.
    \item $x_t^{nuke}$: New nuclear power capacity added in year $t$, for $t = 1, \ldots, T$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total capital cost:
\[
\text{Minimize } \sum_{t=1}^{T} (\text{coal\_cost} \cdot x_t^{coal} + \text{nuke\_cost} \cdot x_t^{nuke})
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Demand Satisfaction Constraint:}
    \[
    \text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} x_i^{coal} + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke} \geq \text{demand}_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Nuclear Capacity Limit:}
    \[
    \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke} \leq \frac{\text{max\_nuke}}{100} \left(\text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} x_i^{coal} + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke}\right), \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Non-negativity:}
    \[
    x_t^{coal} \geq 0, \quad x_t^{nuke} \geq 0, \quad \forall t = 1, \ldots, T
    \]
\end{itemize}

\end{document}
```

This LP model will help find the optimal capacity expansion plan that minimizes the total cost, while satisfying the electricity demand and respecting the nuclear capacity constraint over the planning horizon.

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
\begin{itemize}
    \item $T$: Number of years for planning.
    \item $\text{demand}_t$: Demand for electricity in megawatts in year $t$, for $t = 1, \ldots, T$.
    \item $\text{oil}_t$: Existing oil-fired capacity available in year $t$, for $t = 1, \ldots, T$.
    \item $\text{coal\_cost}$: Capital cost per megawatt for coal-fired capacity.
    \item $\text{nuke\_cost}$: Capital cost per megawatt for nuclear power capacity.
    \item $\text{max\_nuke}$: Maximum percentage of total capacity that can be nuclear.
    \item $\text{coal\_life}$: Lifespan of coal plants in years.
    \item $\text{nuke\_life}$: Lifespan of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{coal}$: New coal-fired capacity added in year $t$, for $t = 1, \ldots, T$.
    \item $x_t^{nuke}$: New nuclear power capacity added in year $t$, for $t = 1, \ldots, T$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total capital cost:
\[
\text{Minimize } \sum_{t=1}^{T} (\text{coal\_cost} \cdot x_t^{coal} + \text{nuke\_cost} \cdot x_t^{nuke})
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Demand Satisfaction Constraint:}
    \[
    \text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} x_i^{coal} + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke} \geq \text{demand}_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Nuclear Capacity Limit:}
    \[
    \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke} \leq \frac{\text{max\_nuke}}{100} \left(\text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} x_i^{coal} + \sum_{i=\max(1, t-\text{nuke\_life}+1)}^{t} x_i^{nuke}\right), \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Non-negativity:}
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
import json

#### Data input
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

#### Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, T + 1), lowBound=0)
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, T + 1), lowBound=0)

#### Objective Function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(1, T + 1))

#### Constraints
for t in range(1, T + 1):
    #### Demand Satisfaction Constraint
    problem += (oil_capacity[t - 1] + 
                 pulp.lpSum(x_coal[i] for i in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1], 
                 f"Demand_Constraint_{t}")

    #### Nuclear Capacity Limit
    problem += (pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1)) <= 
                 (max_nuke / 100) * (oil_capacity[t - 1] + 
                 pulp.lpSum(x_coal[i] for i in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(x_nuke[i] for i in range(max(1, t - nuke_life + 1), t + 1))),
                 f"Nuclear_Capacity_Constraint_{t}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

