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

\section*{Electricity Capacity Expansion Model}

\textbf{Variables:}

Let:
\begin{itemize}
    \item \( C_t \) = capacity of coal-fired power plants added in year \( t \) (in megawatts)
    \item \( N_t \) = capacity of nuclear power plants added in year \( t \) (in megawatts)
    \item \( T \) = total number of years
\end{itemize}

\textbf{Parameters:}

\begin{itemize}
    \item \( \text{demand}_t \) = demand for electricity during year \( t \) (in megawatts)
    \item \( \text{oil}_t \) = existing oil capacity available during year \( t \) (in megawatts)
    \item \( \text{coal\_cost} \) = capital cost per megawatt for coal-fired plants
    \item \( \text{nuke\_cost} \) = capital cost per megawatt for nuclear plants
    \item \( \text{max\_nuke} \) = maximum percentage of total capacity that can be nuclear
    \item \( \text{coal\_life} \) = lifespan of coal plants (in years)
    \item \( \text{nuke\_life} \) = lifespan of nuclear plants (in years)
\end{itemize}

\textbf{Objective Function:}

Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} (\text{coal\_cost} \cdot C_t + \text{nuke\_cost} \cdot N_t)
\]

\textbf{Constraints:}

1. Capacity Constraint:
\[
\text{oil}_t + \sum_{i=1}^{\min(t, \text{coal\_life})} C_{t-i} + \sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \geq \text{demand}_t \quad \forall t \in \{1, \ldots, T\}
\]

2. Nuclear Capacity Limit:
\[
\sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \leq \frac{\text{max\_nuke}}{100} \left( \text{oil}_t + \sum_{i=1}^{\min(t, \text{coal\_life})} C_{t-i} + \sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \right) \quad \forall t \in \{1, \ldots, T\}
\]

3. Non-negativity:
\[
C_t \geq 0, \quad N_t \geq 0 \quad \forall t \in \{1, \ldots, T\}
\]

\textbf{Output:}
The output should be represented as follows:
\begin{verbatim}
{
    "coal_cap_added": [C_1, C_2, ..., C_T],
    "nuke_cap_added": [N_1, N_2, ..., N_T],
    "total_cost": total_cost
}
\end{verbatim}

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

\section*{Electricity Capacity Expansion Model}

\textbf{Variables:}

Let:
\begin{itemize}
    \item \( C_t \) = capacity of coal-fired power plants added in year \( t \) (in megawatts)
    \item \( N_t \) = capacity of nuclear power plants added in year \( t \) (in megawatts)
    \item \( T \) = total number of years
\end{itemize}

\textbf{Parameters:}

\begin{itemize}
    \item \( \text{demand}_t \) = demand for electricity during year \( t \) (in megawatts)
    \item \( \text{oil}_t \) = existing oil capacity available during year \( t \) (in megawatts)
    \item \( \text{coal\_cost} \) = capital cost per megawatt for coal-fired plants
    \item \( \text{nuke\_cost} \) = capital cost per megawatt for nuclear plants
    \item \( \text{max\_nuke} \) = maximum percentage of total capacity that can be nuclear
    \item \( \text{coal\_life} \) = lifespan of coal plants (in years)
    \item \( \text{nuke\_life} \) = lifespan of nuclear plants (in years)
\end{itemize}

\textbf{Objective Function:}

Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} (\text{coal\_cost} \cdot C_t + \text{nuke\_cost} \cdot N_t)
\]

\textbf{Constraints:}

1. Capacity Constraint:
\[
\text{oil}_t + \sum_{i=1}^{\min(t, \text{coal\_life})} C_{t-i} + \sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \geq \text{demand}_t \quad \forall t \in \{1, \ldots, T\}
\]

2. Nuclear Capacity Limit:
\[
\sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \leq \frac{\text{max\_nuke}}{100} \left( \text{oil}_t + \sum_{i=1}^{\min(t, \text{coal\_life})} C_{t-i} + \sum_{j=1}^{\min(t, \text{nuke\_life})} N_{t-j} \right) \quad \forall t \in \{1, \ldots, T\}
\]

3. Non-negativity:
\[
C_t \geq 0, \quad N_t \geq 0 \quad \forall t \in \{1, \ldots, T\}
\]

\textbf{Output:}
The output should be represented as follows:
\begin{verbatim}
{
    "coal_cap_added": [C_1, C_2, ..., C_T],
    "nuke_cap_added": [N_1, N_2, ..., N_T],
    "total_cost": total_cost
}
\end{verbatim}

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

#### Problem Definition
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
C = [pulp.LpVariable(f'C_{t+1}', lowBound=0, cat='Continuous') for t in range(data['T'])]
N = [pulp.LpVariable(f'N_{t+1}', lowBound=0, cat='Continuous') for t in range(data['T'])]

#### Objective Function
problem += pulp.lpSum([data['CoalCost'] * C[t] + data['NukeCost'] * N[t] for t in range(data['T'])])

#### Constraints
for t in range(data['T']):
    coal_life_terms = [C[i] for i in range(max(0, t - data['CoalLife'] + 1), t + 1)]
    nuke_life_terms = [N[j] for j in range(max(0, t - data['NukeLife'] + 1), t + 1)]
    
    #### 1. Capacity Constraint
    problem += (data['OilCap'][t] + pulp.lpSum(coal_life_terms) + pulp.lpSum(nuke_life_terms) >= data['Demand'][t])

    #### 2. Nuclear Capacity Limit
    problem += (pulp.lpSum(nuke_life_terms) <= (data['MaxNuke'] / 100) * (data['OilCap'][t] + pulp.lpSum(coal_life_terms) + pulp.lpSum(nuke_life_terms)))

#### Solve the problem
problem.solve()

#### Output
coal_cap_added = [C[t].varValue for t in range(data['T'])]
nuke_cap_added = [N[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

