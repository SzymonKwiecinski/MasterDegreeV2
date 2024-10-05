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
To formulate the given problem as a linear programming model, we need to define variables, constraints, and the objective function. Let's create a mathematical model with the provided information:

######### Decision Variables

- \( \text{coal\_add}_t \): Number of megawatts of coal-fired capacity added in year \( t \).
- \( \text{nuke\_add}_t \): Number of megawatts of nuclear capacity added in year \( t \).

######### Parameters

- \( \text{demand}_t \): Electricity demand in megawatts for year \( t \).
- \( \text{oil}_t \): Existing oil-fired capacity available in year \( t \).
- \( \text{coal\_cost} \): Capital cost per megawatt for coal-fired capacity.
- \( \text{nuke\_cost} \): Capital cost per megawatt for nuclear capacity.
- \( \text{max\_nuke} \): Maximum percentage of total capacity that can be nuclear.
- \( \text{coal\_life} \): Lifespan of coal plants in years.
- \( \text{nuke\_life} \): Lifespan of nuclear plants in years.

######### Objective Function

Minimize the total cost of capacity expansion:

\[
\text{Minimize} \quad \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t \right)
\]

######### Constraints

1. **Demand Satisfaction:**
   \[
   \sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \geq \text{demand}_t \quad \forall t
   \]

2. **Nuclear Capacity Limit:**
   \[
   \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau \leq \frac{\text{max\_nuke}}{100} \left( \sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \right) \quad \forall t
   \]

3. **Non-negativity:**
   \[
   \text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0 \quad \forall t
   \]

This model will help determine how much coal and nuclear capacity should be added in each year to meet the demand at minimum cost while adhering to the capacity restrictions.

Here is the complete model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\textbf{Decision Variables:}
\begin{align*}
\text{coal\_add}_t &: \text{Number of megawatts of coal-fired capacity added in year } t. \\
\text{nuke\_add}_t &: \text{Number of megawatts of nuclear capacity added in year } t. 
\end{align*}

\textbf{Objective: Minimize the total cost of capacity expansion}
\[
\text{Minimize} \quad \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t \right)
\]

\textbf{Constraints:}

1. \textbf{Demand Satisfaction:}
\[
\sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \geq \text{demand}_t \quad \forall t
\]

2. \textbf{Nuclear Capacity Limit:}
\[
\sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau \leq \frac{\text{max\_nuke}}{100} \left( \sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \right) \quad \forall t
\]

3. \textbf{Non-negativity:}
\[
\text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0 \quad \forall t
\]

\end{document}
```

This mathematical model can be used to solve the problem using linear programming techniques, ensuring that the capacity expansion plan is both cost-effective and compliant with the specified constraints.

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

\textbf{Decision Variables:}
\begin{align*}
\text{coal\_add}_t &: \text{Number of megawatts of coal-fired capacity added in year } t. \\
\text{nuke\_add}_t &: \text{Number of megawatts of nuclear capacity added in year } t. 
\end{align*}

\textbf{Objective: Minimize the total cost of capacity expansion}
\[
\text{Minimize} \quad \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t \right)
\]

\textbf{Constraints:}

1. \textbf{Demand Satisfaction:}
\[
\sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \geq \text{demand}_t \quad \forall t
\]

2. \textbf{Nuclear Capacity Limit:}
\[
\sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau \leq \frac{\text{max\_nuke}}{100} \left( \sum_{\tau=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_\tau + \sum_{\tau=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_\tau + \text{oil}_t \right) \quad \forall t
\]

3. \textbf{Non-negativity:}
\[
\text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0 \quad \forall t
\]

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

#### Indices
T = data['T']

#### Create the Linear Programming problem
problem = pulp.LpProblem("Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_add = pulp.LpVariable.dicts("coal_add", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_add = pulp.LpVariable.dicts("nuke_add", range(1, T + 1), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum([data['CoalCost'] * coal_add[t] + data['NukeCost'] * nuke_add[t] for t in range(1, T + 1)])

#### Constraints
for t in range(1, T + 1):
    coal_accum = pulp.lpSum(coal_add[tau] for tau in range(max(1, t - data['CoalLife'] + 1), t + 1))
    nuke_accum = pulp.lpSum(nuke_add[tau] for tau in range(max(1, t - data['NukeLife'] + 1), t + 1))

    #### Demand Satisfaction
    problem += (coal_accum + nuke_accum + data['OilCap'][t - 1] >= data['Demand'][t - 1])

    #### Nuclear Capacity Limit
    problem += (nuke_accum <= data['MaxNuke'] / 100 * (coal_accum + nuke_accum + data['OilCap'][t - 1]))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

