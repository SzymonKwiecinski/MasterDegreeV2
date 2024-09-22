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
To solve this problem, we need to formulate a linear programming model that minimizes the total cost of electricity capacity expansion over the planning horizon of \( T \) years. We will include decision variables for coal and nuclear capacity additions, constraints to ensure demand is met, and a constraint to limit the proportion of nuclear energy. Let's define the model in LaTeX.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{itemize}
    \item \( T \): Number of years in the planning period
    \item \( \text{demand}_t \): Forecasted demand for electricity in year \( t \), for \( t = 1, \ldots, T \)
    \item \( \text{oil}_t \): Existing oil capacity available in year \( t \), for \( t = 1, \ldots, T \)
    \item \( \text{coal\_cost} \): Capital cost per megawatt of coal-fired capacity
    \item \( \text{nuke\_cost} \): Capital cost per megawatt of nuclear capacity
    \item \( \text{max\_nuke} \): Maximum percentage of total capacity that can be nuclear
    \item \( \text{coal\_life} \): Lifetime of coal plants (in years)
    \item \( \text{nuke\_life} \): Lifetime of nuclear plants (in years)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{coal\_added}_t \): Coal-fired capacity added at the beginning of year \( t \)
    \item \( \text{nuke\_added}_t \): Nuclear capacity added at the beginning of year \( t \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost over \( T \) years:
\[
\text{Minimize} \quad \sum_{t=1}^{T} (\text{coal\_cost} \cdot \text{coal\_added}_t + \text{nuke\_cost} \cdot \text{nuke\_added}_t)
\]

\subsection*{Constraints}
1. Demand satisfaction for each year \( t \):
\[
\text{oil}_t + \sum_{k=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_added}_k + \sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k \geq \text{demand}_t \quad \forall t = 1, \ldots, T
\]

2. Nuclear proportion constraint:
\[
\frac{\sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k}{\text{oil}_t + \sum_{k=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_added}_k + \sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k} \leq \frac{\text{max\_nuke}}{100} \quad \forall t = 1, \ldots, T
\]

3. Non-negativity constraints:
\[
\text{coal\_added}_t \geq 0, \quad \text{nuke\_added}_t \geq 0 \quad \forall t = 1, \ldots, T
\]

\end{document}
```

This LaTeX document clearly defines the linear programming model needed to determine the optimal capacity expansion plan. The objective is to minimize the total cost of adding new capacities while satisfying future electricity demand and meeting the constraint on nuclear proportion. Each constraint and component of the objective function is crucial to achieving an optimal and feasible solution.

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
    \item \( T \): Number of years in the planning period
    \item \( \text{demand}_t \): Forecasted demand for electricity in year \( t \), for \( t = 1, \ldots, T \)
    \item \( \text{oil}_t \): Existing oil capacity available in year \( t \), for \( t = 1, \ldots, T \)
    \item \( \text{coal\_cost} \): Capital cost per megawatt of coal-fired capacity
    \item \( \text{nuke\_cost} \): Capital cost per megawatt of nuclear capacity
    \item \( \text{max\_nuke} \): Maximum percentage of total capacity that can be nuclear
    \item \( \text{coal\_life} \): Lifetime of coal plants (in years)
    \item \( \text{nuke\_life} \): Lifetime of nuclear plants (in years)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{coal\_added}_t \): Coal-fired capacity added at the beginning of year \( t \)
    \item \( \text{nuke\_added}_t \): Nuclear capacity added at the beginning of year \( t \)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost over \( T \) years:
\[
\text{Minimize} \quad \sum_{t=1}^{T} (\text{coal\_cost} \cdot \text{coal\_added}_t + \text{nuke\_cost} \cdot \text{nuke\_added}_t)
\]

\subsection*{Constraints}
1. Demand satisfaction for each year \( t \):
\[
\text{oil}_t + \sum_{k=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_added}_k + \sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k \geq \text{demand}_t \quad \forall t = 1, \ldots, T
\]

2. Nuclear proportion constraint:
\[
\frac{\sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k}{\text{oil}_t + \sum_{k=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_added}_k + \sum_{k=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_added}_k} \leq \frac{\text{max\_nuke}}{100} \quad \forall t = 1, \ldots, T
\]

3. Non-negativity constraints:
\[
\text{coal\_added}_t \geq 0, \quad \text{nuke\_added}_t \geq 0 \quad \forall t = 1, \ldots, T
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

#### Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_added = [pulp.LpVariable(f"coal_added_{t}", lowBound=0, cat='Continuous') for t in range(data['T'])]
nuke_added = [pulp.LpVariable(f"nuke_added_{t}", lowBound=0, cat='Continuous') for t in range(data['T'])]

#### Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal_added[t] + data['NukeCost'] * nuke_added[t] for t in range(data['T']))

#### Constraints
for t in range(data['T']):
    coal_lifetime_sum = pulp.lpSum(coal_added[k] for k in range(max(0, t - data['CoalLife'] + 1), t + 1))
    nuke_lifetime_sum = pulp.lpSum(nuke_added[k] for k in range(max(0, t - data['NukeLife'] + 1), t + 1))
    
    #### Demand satisfaction
    problem += data['OilCap'][t] + coal_lifetime_sum + nuke_lifetime_sum >= data['Demand'][t]
    
    #### Nuclear proportion constraint
    total_capacity = data['OilCap'][t] + coal_lifetime_sum + nuke_lifetime_sum
    problem += nuke_lifetime_sum <= data['MaxNuke'] / 100 * total_capacity

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

