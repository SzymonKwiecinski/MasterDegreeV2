# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP
PROBLEM INFO:

- A number of power stations are committed to meeting the following electricity load demands over a day.
- Period \var{t} of a day has demand \var{demand_{t}}.
- There are several types of generating unit available: the number of \var{k}-th type units is \var{num_{k}}.
- Type \var{k} generator has to work between a minimum level \var{minlevel_{k}} and a maximum level \var{maxlevel_{k}}. 
- There is an hourly cost of running each type \var{k} generator at minimum level \var{runcost_{k}}. 
- In addition, there is an extra hourly cost \var{extracost_{k}} for each megawatt at which a type \var{k} unit is operated above the minimum level. 
- Starting up a type \var{k} generator also involves a cost \var{startcost_{k}}.


INPUT FORMAT:

{
    "demand": [demand_{t} for t in 1,...,T],
    "num": [num_{k} for in 1,...,K],
    "minlevel": [minlevel_{k} for in 1,...,K],
    "maxlevel": [minlevel_{k} for in 1,...,K],
    "runcost": [runcost_{k} for in 1,...,K],
    "extracost": [extracost_{k} for in 1,...,K],
    "startcost": [startcost_{k} for in 1,...,K]
}


OBJECTIVE: Which generators should be working in which periods of the day to minimize total cost?

OUTPUT INFO:

- \var{numon} represents the number of generators of each type that are on in each period

OUTPUT FORMAT:

{
    "numon": [[numon_{k, t} for t in 1,...,T] for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Power Generation Scheduling}

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( T \) be the number of time periods in a day.
    \item Let \( K \) be the number of types of generating units.
    \item Let \( demand_t \) be the electricity demand at time period \( t \) for \( t = 1, \ldots, T \).
    \item Let \( num_k \) be the number of units of type \( k \) available for \( k = 1, \ldots, K \).
    \item Let \( minlevel_k \) be the minimum operational level of type \( k \).
    \item Let \( maxlevel_k \) be the maximum operational level of type \( k \).
    \item Let \( runcost_k \) be the hourly cost of running each type \( k \) generator at minimum level.
    \item Let \( extracost_k \) be the additional cost per megawatt for each type \( k \) generator operated above the minimum level.
    \item Let \( startcost_k \) be the startup cost for type \( k \) generators.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( numon_{k,t} \) be the number of generators of type \( k \) that are on during time period \( t \).
    \item Let \( level_{k,t} \) be the operational level of type \( k \) generators during time period \( t \). 
    \item Let \( start_{k,t} \) be a binary variable indicating whether type \( k \) generator is started at time period \( t \) (1 if started, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot \max(0, level_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot start_{k,t} \right)
\]

\subsection*{Constraints}
1. **Demand Satisfaction:**
\[
\sum_{k=1}^{K} level_{k,t} = demand_t \quad \forall t = 1, \ldots, T
\]

2. **Operational Level Constraints:**
\[
minlevel_k \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

3. **Generator Availability:**
\[
numon_{k,t} \leq num_k \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

4. **Startup Indicator:**
\[
level_{k,t} \leq maxlevel_k \cdot start_{k,t} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

5. **Binary Variable Constraints:**
\[
start_{k,t} \in \{0, 1\} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
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

\section*{Mathematical Model for Power Generation Scheduling}

\subsection*{Sets and Parameters}
\begin{itemize}
    \item Let \( T \) be the number of time periods in a day.
    \item Let \( K \) be the number of types of generating units.
    \item Let \( demand_t \) be the electricity demand at time period \( t \) for \( t = 1, \ldots, T \).
    \item Let \( num_k \) be the number of units of type \( k \) available for \( k = 1, \ldots, K \).
    \item Let \( minlevel_k \) be the minimum operational level of type \( k \).
    \item Let \( maxlevel_k \) be the maximum operational level of type \( k \).
    \item Let \( runcost_k \) be the hourly cost of running each type \( k \) generator at minimum level.
    \item Let \( extracost_k \) be the additional cost per megawatt for each type \( k \) generator operated above the minimum level.
    \item Let \( startcost_k \) be the startup cost for type \( k \) generators.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( numon_{k,t} \) be the number of generators of type \( k \) that are on during time period \( t \).
    \item Let \( level_{k,t} \) be the operational level of type \( k \) generators during time period \( t \). 
    \item Let \( start_{k,t} \) be a binary variable indicating whether type \( k \) generator is started at time period \( t \) (1 if started, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Total Cost} = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot \max(0, level_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot start_{k,t} \right)
\]

\subsection*{Constraints}
1. **Demand Satisfaction:**
\[
\sum_{k=1}^{K} level_{k,t} = demand_t \quad \forall t = 1, \ldots, T
\]

2. **Operational Level Constraints:**
\[
minlevel_k \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

3. **Generator Availability:**
\[
numon_{k,t} \leq num_k \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

4. **Startup Indicator:**
\[
level_{k,t} \leq maxlevel_k \cdot start_{k,t} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

5. **Binary Variable Constraints:**
\[
start_{k,t} \in \{0, 1\} \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

T = len(data['demand'])  #### number of time periods
K = len(data['num'])  #### number of types of generating units

#### Create the problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, cat='Continuous')
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                       data['extracost'][k] * pulp.lpSum(level[k][t] - data['minlevel'][k] * numon[k][t]) +
                       data['startcost'][k] * start[k][t]
                       for t in range(T) for k in range(K))

#### Constraints
#### Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == data['demand'][t]

#### Operational Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= level[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]

#### Generator Availability
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

#### Startup Indicator
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= data['maxlevel'][k] * start[k][t]

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

