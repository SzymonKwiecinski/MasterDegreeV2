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
    \item \( T \): Number of years.
    \item \( d_t \): Demand for electricity in year \( t \), for \( t = 1, \ldots, T \).
    \item \( oil_t \): Existing oil-fired capacity available in year \( t \).
    \item \( coal\_cost \): Capital cost per megawatt of coal-fired capacity.
    \item \( nuke\_cost \): Capital cost per megawatt of nuclear power capacity.
    \item \( max\_nuke \): Maximum percentage of total capacity that can be nuclear.
    \item \( coal\_life \): Lifespan of coal plants (in years).
    \item \( nuke\_life \): Lifespan of nuclear plants (in years).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( coal_t \): Capacity of coal added in year \( t \).
    \item \( nuke_t \): Capacity of nuclear added in year \( t \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of capacity expansion:
\[
\text{Minimize } Z = \sum_{t=1}^{T} (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\]

\subsection*{Constraints}
1. Capacity demand constraints:
\[
oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j} \geq d_t, \quad \forall t = 1, \ldots, T
\]
2. Maximum nuclear capacity constraint:
\[
\sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j} \cdot \frac{nuke\_cost}{coal\_cost} \leq \frac{max\_nuke}{100} \cdot (oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j}), \quad \forall t = 1, \ldots, T
\]

\subsection*{Output Format}
The output should provide the following information:
\begin{itemize}
    \item \texttt{coal\_cap\_added}: List of coal capacity added each year.
    \item \texttt{nuke\_cap\_added}: List of nuclear capacity added each year.
    \item \texttt{total\_cost}: Total cost of the capacity expansion.
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

\section*{Mathematical Model for Electricity Capacity Expansion}

\subsection*{Parameters}
\begin{itemize}
    \item \( T \): Number of years.
    \item \( d_t \): Demand for electricity in year \( t \), for \( t = 1, \ldots, T \).
    \item \( oil_t \): Existing oil-fired capacity available in year \( t \).
    \item \( coal\_cost \): Capital cost per megawatt of coal-fired capacity.
    \item \( nuke\_cost \): Capital cost per megawatt of nuclear power capacity.
    \item \( max\_nuke \): Maximum percentage of total capacity that can be nuclear.
    \item \( coal\_life \): Lifespan of coal plants (in years).
    \item \( nuke\_life \): Lifespan of nuclear plants (in years).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( coal_t \): Capacity of coal added in year \( t \).
    \item \( nuke_t \): Capacity of nuclear added in year \( t \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of capacity expansion:
\[
\text{Minimize } Z = \sum_{t=1}^{T} (coal\_cost \cdot coal_t + nuke\_cost \cdot nuke_t)
\]

\subsection*{Constraints}
1. Capacity demand constraints:
\[
oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j} \geq d_t, \quad \forall t = 1, \ldots, T
\]
2. Maximum nuclear capacity constraint:
\[
\sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j} \cdot \frac{nuke\_cost}{coal\_cost} \leq \frac{max\_nuke}{100} \cdot (oil_t + \sum_{j=1}^{\min(t, coal\_life)} coal_{t-j} + \sum_{j=1}^{\min(t, nuke\_life)} nuke_{t-j}), \quad \forall t = 1, \ldots, T
\]

\subsection*{Output Format}
The output should provide the following information:
\begin{itemize}
    \item \texttt{coal\_cap\_added}: List of coal capacity added each year.
    \item \texttt{nuke\_cap\_added}: List of nuclear capacity added each year.
    \item \texttt{total\_cost}: Total cost of the capacity expansion.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
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

#### Create the problem variable
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Decision Variables
coal = pulp.LpVariable.dicts("coal", range(T), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("nuke", range(T), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(T))

#### Capacity demand constraints
for t in range(T):
    problem += (oil_capacity[t] +
                 pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1)) >= demand[t])

#### Maximum nuclear capacity constraint
for t in range(T):
    problem += (pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1)) * (nuke_cost / coal_cost) <= 
                 (max_nuke / 100) * (oil_capacity[t] +
                 pulp.lpSum(coal[t-j] for j in range(1, min(t, coal_life) + 1)) +
                 pulp.lpSum(nuke[t-j] for j in range(1, min(t, nuke_life) + 1))))

#### Solve the problem
problem.solve()

#### Prepare output
coal_capacity_added = [coal[t].varValue for t in range(T)]
nuke_capacity_added = [nuke[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

#### Print results
print(f'Coal capacity added each year: {coal_capacity_added}')
print(f'Nuclear capacity added each year: {nuke_capacity_added}')
print(f'Total cost of capacity expansion: <OBJ>{total_cost}</OBJ>')
```

