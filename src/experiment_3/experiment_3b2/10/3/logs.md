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
To solve this linear programming problem, we will formulate a mathematical model representing the capacity planning decision. The objective is to minimize the total cost of expanding the electric capacity while satisfying all the constraints. Here's the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Electricity Capacity Planning}

Let:
\begin{itemize}
    \item \( T \) be the total number of years for planning.
    \item \( \text{demand}_t \) be the forecasted electricity demand in year \( t \).
    \item \( \text{oil}_t \) be the existing capacity of oil-fired plants in year \( t \).
    \item \( \text{coal\_cost} \) be the cost per megawatt of coal-fired capacity.
    \item \( \text{nuke\_cost} \) be the cost per megawatt of nuclear power capacity.
    \item \( \text{max\_nuke} \) be the maximum percentage of total capacity that can be nuclear.
    \item \( \text{coal\_life} \) be the lifespan of coal plants in years.
    \item \( \text{nuke\_life} \) be the lifespan of nuclear plants in years.
    \item \( \text{coal\_cap\_added}_t \) be the coal capacity added in year \( t \).
    \item \( \text{nuke\_cap\_added}_t \) be the nuclear capacity added in year \( t \).
\end{itemize}

\textbf{Objective:}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t \right)
\]

\textbf{Subject to:}
\begin{align}
    & \text{Coal and Nuclear Capacity Balance:} \\
    & \sum_{i = \max(1, t - \text{coal\_life} + 1)}^{t} \text{coal\_cap\_added}_i + \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j + \text{oil}_t \geq \text{demand}_t, \quad \forall t = 1, \ldots, T \\
    & \text{Nuclear Capacity Constraint:} \\
    & \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j \leq \frac{\text{max\_nuke}}{100} \left(\sum_{i = \max(1, t - \text{coal\_life} + 1)}^{t} \text{coal\_cap\_added}_i + \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j + \text{oil}_t \right), \quad \forall t = 1, \ldots, T \\
    & \text{Non-negativity Constraints:} \\
    & \text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t = 1, \ldots, T
\end{align}

\end{document}
```

This LaTeX code describes the linear programming model for electricity capacity planning by minimizing total costs while satisfying demand and nuclear capacity constraints over a planning horizon of \( T \) years. The decision variables \( \text{coal\_cap\_added}_t \) and \( \text{nuke\_cap\_added}_t \) represent the new capacities added each year, subject to meeting demands, lifespan constraints, and nuclear percentage restrictions.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Electricity Capacity Planning}

Let:
\begin{itemize}
    \item \( T \) be the total number of years for planning.
    \item \( \text{demand}_t \) be the forecasted electricity demand in year \( t \).
    \item \( \text{oil}_t \) be the existing capacity of oil-fired plants in year \( t \).
    \item \( \text{coal\_cost} \) be the cost per megawatt of coal-fired capacity.
    \item \( \text{nuke\_cost} \) be the cost per megawatt of nuclear power capacity.
    \item \( \text{max\_nuke} \) be the maximum percentage of total capacity that can be nuclear.
    \item \( \text{coal\_life} \) be the lifespan of coal plants in years.
    \item \( \text{nuke\_life} \) be the lifespan of nuclear plants in years.
    \item \( \text{coal\_cap\_added}_t \) be the coal capacity added in year \( t \).
    \item \( \text{nuke\_cap\_added}_t \) be the nuclear capacity added in year \( t \).
\end{itemize}

\textbf{Objective:}
Minimize the total cost:
\[
\text{Minimize} \quad \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_cap\_added}_t + \text{nuke\_cost} \times \text{nuke\_cap\_added}_t \right)
\]

\textbf{Subject to:}
\begin{align}
    & \text{Coal and Nuclear Capacity Balance:} \\
    & \sum_{i = \max(1, t - \text{coal\_life} + 1)}^{t} \text{coal\_cap\_added}_i + \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j + \text{oil}_t \geq \text{demand}_t, \quad \forall t = 1, \ldots, T \\
    & \text{Nuclear Capacity Constraint:} \\
    & \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j \leq \frac{\text{max\_nuke}}{100} \left(\sum_{i = \max(1, t - \text{coal\_life} + 1)}^{t} \text{coal\_cap\_added}_i + \sum_{j = \max(1, t - \text{nuke\_life} + 1)}^{t} \text{nuke\_cap\_added}_j + \text{oil}_t \right), \quad \forall t = 1, \ldots, T \\
    & \text{Non-negativity Constraints:} \\
    & \text{coal\_cap\_added}_t \geq 0, \quad \text{nuke\_cap\_added}_t \geq 0, \quad \forall t = 1, \ldots, T
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')

#### Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

#### Variables for coal and nuclear capacity additions
coal_cap_added = pulp.LpVariable.dicts("coal_cap_added", range(1, data['T'] + 1), lowBound=0)
nuke_cap_added = pulp.LpVariable.dicts("nuke_cap_added", range(1, data['T'] + 1), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['CoalCost'] * coal_cap_added[t] + data['NukeCost'] * nuke_cap_added[t] for t in range(1, data['T'] + 1))

#### Constraints
for t in range(1, data['T'] + 1):
    #### Coal and Nuclear Capacity Balance
    coal_capacity = pulp.lpSum(coal_cap_added[i] for i in range(max(1, t - data['CoalLife'] + 1), t + 1))
    nuke_capacity = pulp.lpSum(nuke_cap_added[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (coal_capacity + nuke_capacity + data['OilCap'][t - 1] >= data['Demand'][t - 1]), f"Capacity_Balance_{t}"
    
    #### Nuclear Capacity Constraint
    problem += (nuke_capacity <= (data['MaxNuke'] / 100) * (coal_capacity + nuke_capacity + data['OilCap'][t - 1])), f"Nuclear_Capacity_Constraint_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

