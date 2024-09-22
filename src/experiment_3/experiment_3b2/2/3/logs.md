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
To address this optimization problem using Linear Programming (LP), we need to define the decision variables, objective function, and constraints in mathematical terms. Let's denote:

- \( x_t^{coal} \) as the megawatts of coal capacity added in year \( t \)
- \( x_t^{nuke} \) as the megawatts of nuclear capacity added in year \( t \)

Given the input format and problem description, here is the LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: Minimize Total Cost}

\begin{align*}
\text{Minimize} \quad & \sum_{t=1}^{T} \left( \text{coal\_cost} \times x_t^{coal} + \text{nuke\_cost} \times x_t^{nuke} \right)
\end{align*}

\textbf{Subject to:}

1. \textbf{Capacity Constraints:}
\begin{align*}
& \text{For each } t \in \{1, \ldots, T\}, \\
& \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{coal} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} + \text{oil\_cap}[t-1] \geq \text{demand}[t-1]
\end{align*}

2. \textbf{Nuclear Capacity Constraint:}
\begin{align*}
& \text{For each } t \in \{1, \ldots, T\}, \\
& \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} \leq \frac{\text{max\_nuke}}{100} \times \left( \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{coal} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} + \text{oil\_cap}[t-1] \right)
\end{align*}

3. \textbf{Non-negativity Constraints:}
\begin{align*}
& x_t^{coal} \geq 0 \quad \text{and} \quad x_t^{nuke} \geq 0 \quad \text{for all } t.
\end{align*}

\end{document}
```

This LP formulation ensures that we meet the electricity demand each year, respect the maximum nuclear capacity constraint, and keep costs minimal. By solving this LP, you can determine the optimal capacity expansion plan that minimizes costs while satisfying all constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective: Minimize Total Cost}

\begin{align*}
\text{Minimize} \quad & \sum_{t=1}^{T} \left( \text{coal\_cost} \times x_t^{coal} + \text{nuke\_cost} \times x_t^{nuke} \right)
\end{align*}

\textbf{Subject to:}

1. \textbf{Capacity Constraints:}
\begin{align*}
& \text{For each } t \in \{1, \ldots, T\}, \\
& \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{coal} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} + \text{oil\_cap}[t-1] \geq \text{demand}[t-1]
\end{align*}

2. \textbf{Nuclear Capacity Constraint:}
\begin{align*}
& \text{For each } t \in \{1, \ldots, T\}, \\
& \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} \leq \frac{\text{max\_nuke}}{100} \times \left( \sum_{j=\max(1, t-\text{coal\_life}+1)}^{t} x_j^{coal} + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} x_j^{nuke} + \text{oil\_cap}[t-1] \right)
\end{align*}

3. \textbf{Non-negativity Constraints:}
\begin{align*}
& x_t^{coal} \geq 0 \quad \text{and} \quad x_t^{nuke} \geq 0 \quad \text{for all } t.
\end{align*}

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
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

#### Decision variables
x_coal = pulp.LpVariable.dicts("x_coal", range(1, data['T'] + 1), lowBound=0)
x_nuke = pulp.LpVariable.dicts("x_nuke", range(1, data['T'] + 1), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['CoalCost'] * x_coal[t] + data['NukeCost'] * x_nuke[t] for t in range(1, data['T'] + 1))

#### Capacity constraints
for t in range(1, data['T'] + 1):
    problem += (
        pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
        data['OilCap'][t - 1] >= data['Demand'][t - 1]
    )

#### Nuclear capacity constraints
for t in range(1, data['T'] + 1):
    problem += (
        pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) <=
        (data['MaxNuke'] / 100) * (
            pulp.lpSum(x_coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1)) +
            pulp.lpSum(x_nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1)) +
            data['OilCap'][t - 1]
        )
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

