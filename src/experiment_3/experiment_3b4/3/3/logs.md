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

We are tasked with planning the electricity capacity expansion for the next \( T \) years using the following input parameters:

\begin{itemize}
    \item Forecasted electricity demand for year \( t \): \( \text{demand}_t \)
    \item Existing oil-fired plant capacity for year \( t \): \( \text{oil}_t \)
    \item Capital cost per megawatt of coal-fired capacity: \( \text{coal\_cost} \)
    \item Capital cost per megawatt of nuclear power capacity: \( \text{nuke\_cost} \)
    \item Maximum percentage of nuclear capacity allowed: \( \text{max\_nuke} \)
    \item Lifetime of coal plants in years: \( \text{coal\_life} \)
    \item Lifetime of nuclear plants in years: \( \text{nuke\_life} \)
\end{itemize}

\subsection*{Decision Variables}

\begin{align*}
    \text{coal\_add}_t & : \text{Megawatts of coal capacity added in year } t, \quad t = 1, \ldots, T \\
    \text{nuke\_add}_t & : \text{Megawatts of nuclear capacity added in year } t, \quad t = 1, \ldots, T 
\end{align*}

\subsection*{Objective Function}

Minimize the total cost of capacity expansion:

\[
\text{Minimize} \quad Z = \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t \right)
\]

\subsection*{Constraints}

1. \textbf{Demand Satisfaction Constraint:} Total capacity must meet or exceed demand for each year \( t \).

\[
\text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_i + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \geq \text{demand}_t, \quad t = 1, \ldots, T
\]

2. \textbf{Nuclear Capacity Constraint:} Limit on the percentage of total capacity that can be nuclear.

\[
\left( \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \right) \leq \frac{\text{max\_nuke}}{100} \times \left( \text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_i + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \right), \quad t = 1, \ldots, T
\]

3. \textbf{Non-negativity Constraints:}

\[
\text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0, \quad t = 1, \ldots, T
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

\section*{Linear Programming Model for Electricity Capacity Expansion}

We are tasked with planning the electricity capacity expansion for the next \( T \) years using the following input parameters:

\begin{itemize}
    \item Forecasted electricity demand for year \( t \): \( \text{demand}_t \)
    \item Existing oil-fired plant capacity for year \( t \): \( \text{oil}_t \)
    \item Capital cost per megawatt of coal-fired capacity: \( \text{coal\_cost} \)
    \item Capital cost per megawatt of nuclear power capacity: \( \text{nuke\_cost} \)
    \item Maximum percentage of nuclear capacity allowed: \( \text{max\_nuke} \)
    \item Lifetime of coal plants in years: \( \text{coal\_life} \)
    \item Lifetime of nuclear plants in years: \( \text{nuke\_life} \)
\end{itemize}

\subsection*{Decision Variables}

\begin{align*}
    \text{coal\_add}_t & : \text{Megawatts of coal capacity added in year } t, \quad t = 1, \ldots, T \\
    \text{nuke\_add}_t & : \text{Megawatts of nuclear capacity added in year } t, \quad t = 1, \ldots, T 
\end{align*}

\subsection*{Objective Function}

Minimize the total cost of capacity expansion:

\[
\text{Minimize} \quad Z = \sum_{t=1}^{T} \left( \text{coal\_cost} \times \text{coal\_add}_t + \text{nuke\_cost} \times \text{nuke\_add}_t \right)
\]

\subsection*{Constraints}

1. \textbf{Demand Satisfaction Constraint:} Total capacity must meet or exceed demand for each year \( t \).

\[
\text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_i + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \geq \text{demand}_t, \quad t = 1, \ldots, T
\]

2. \textbf{Nuclear Capacity Constraint:} Limit on the percentage of total capacity that can be nuclear.

\[
\left( \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \right) \leq \frac{\text{max\_nuke}}{100} \times \left( \text{oil}_t + \sum_{i=\max(1, t-\text{coal\_life}+1)}^{t} \text{coal\_add}_i + \sum_{j=\max(1, t-\text{nuke\_life}+1)}^{t} \text{nuke\_add}_j \right), \quad t = 1, \ldots, T
\]

3. \textbf{Non-negativity Constraints:}

\[
\text{coal\_add}_t \geq 0, \quad \text{nuke\_add}_t \geq 0, \quad t = 1, \ldots, T
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define data
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
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke']
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

#### Initialize problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal_add = [pulp.LpVariable(f"coal_add_{t}", lowBound=0, cat='Continuous') for t in range(T)]
nuke_add = [pulp.LpVariable(f"nuke_add_{t}", lowBound=0, cat='Continuous') for t in range(T)]

#### Objective Function
Z = pulp.lpSum([CoalCost * coal_add[t] + NukeCost * nuke_add[t] for t in range(T)])
problem += Z

#### Constraints
for t in range(T):
    #### Demand Satisfaction Constraint
    problem += (
        OilCap[t] + 
        sum(coal_add[i] for i in range(max(0, t - CoalLife + 1), t + 1)) + 
        sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1)) 
        >= Demand[t]
    )
    
    #### Nuclear Capacity Constraint
    problem += (
        sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1)) 
        <= MaxNuke / 100 * (
            OilCap[t] + 
            sum(coal_add[i] for i in range(max(0, t - CoalLife + 1), t + 1)) + 
            sum(nuke_add[j] for j in range(max(0, t - NukeLife + 1), t + 1))
        )
    )

#### Solve problem
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

