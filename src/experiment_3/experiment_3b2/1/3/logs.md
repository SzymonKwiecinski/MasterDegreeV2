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

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $t \in \{1, 2, \ldots, T\}$: Time periods (years).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $demand_t$: Forecasted demand for electricity in megawatts for year $t$.
    \item $oil_t$: Existing oil-fired capacity available in megawatts for year $t$.
    \item $coal\_cost$: Capital cost per megawatt for coal-fired capacity.
    \item $nuke\_cost$: Capital cost per megawatt for nuclear capacity.
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear.
    \item $coal\_life$: Lifetime of coal plants in years.
    \item $nuke\_life$: Lifetime of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{\text{coal}}$: Megawatts of coal-fired capacity added in year $t$.
    \item $x_t^{\text{nuke}}$: Megawatts of nuclear capacity added in year $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of capacity addition:

\[
\min \sum_{t=1}^{T} \left( coal\_cost \cdot x_t^{\text{coal}} + nuke\_cost \cdot x_t^{\text{nuke}} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:} For each year $t$, the total capacity should meet or exceed the demand.
    \[
    oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \geq demand_t, \quad \forall t
    \]

    \item \textbf{Nuclear Capacity Limit:} The nuclear capacity should not exceed the specified percentage of total capacity.
    \[
    \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \leq \frac{max\_nuke}{100} \cdot \left(oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \right), \quad \forall t
    \]

    \item \textbf{Non-negativity:}
    \[
    x_t^{\text{coal}} \geq 0, \quad x_t^{\text{nuke}} \geq 0, \quad \forall t
    \]
\end{itemize}

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

\section*{Linear Programming Model for Electricity Capacity Planning}

\subsection*{Sets and Indices}
\begin{itemize}
    \item $t \in \{1, 2, \ldots, T\}$: Time periods (years).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $demand_t$: Forecasted demand for electricity in megawatts for year $t$.
    \item $oil_t$: Existing oil-fired capacity available in megawatts for year $t$.
    \item $coal\_cost$: Capital cost per megawatt for coal-fired capacity.
    \item $nuke\_cost$: Capital cost per megawatt for nuclear capacity.
    \item $max\_nuke$: Maximum percentage of total capacity that can be nuclear.
    \item $coal\_life$: Lifetime of coal plants in years.
    \item $nuke\_life$: Lifetime of nuclear plants in years.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_t^{\text{coal}}$: Megawatts of coal-fired capacity added in year $t$.
    \item $x_t^{\text{nuke}}$: Megawatts of nuclear capacity added in year $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of capacity addition:

\[
\min \sum_{t=1}^{T} \left( coal\_cost \cdot x_t^{\text{coal}} + nuke\_cost \cdot x_t^{\text{nuke}} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:} For each year $t$, the total capacity should meet or exceed the demand.
    \[
    oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \geq demand_t, \quad \forall t
    \]

    \item \textbf{Nuclear Capacity Limit:} The nuclear capacity should not exceed the specified percentage of total capacity.
    \[
    \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \leq \frac{max\_nuke}{100} \cdot \left(oil_t + \sum_{j=\max(1, t-coal\_life+1)}^{t} x_j^{\text{coal}} + \sum_{j=\max(1, t-nuke\_life+1)}^{t} x_j^{\text{nuke}} \right), \quad \forall t
    \]

    \item \textbf{Non-negativity:}
    \[
    x_t^{\text{coal}} \geq 0, \quad x_t^{\text{nuke}} \geq 0, \quad \forall t
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

#### Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

#### Decision Variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

#### Constraints
for t in range(1, data['T'] + 1):
    #### Demand Satisfaction
    demand_constraint = (
        data['OilCap'][t - 1] +
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    )
    problem += demand_constraint >= data['Demand'][t - 1]

    #### Nuclear Capacity Limit
    max_nuke_constraint = pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    total_capacity = (
        data['OilCap'][t - 1] +
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    )
    problem += max_nuke_constraint <= (data['MaxNuke'] / 100) * total_capacity

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

