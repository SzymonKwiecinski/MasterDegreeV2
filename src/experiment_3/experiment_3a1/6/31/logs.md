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

\section*{Mathematical Model}

\subsection*{Sets}
\begin{itemize}
  \item $T$: Set of time periods in a day, $t = 1, \ldots, T$.
  \item $K$: Set of generator types, $k = 1, \ldots, K$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
  \item $demand_t$: Electricity demand during period $t$.
  \item $num_k$: Number of available generators of type $k$.
  \item $minlevel_k$: Minimum operating level of generator type $k$.
  \item $maxlevel_k$: Maximum operating level of generator type $k$.
  \item $runcost_k$: Hourly cost of running each generator of type $k$ at minimum level.
  \item $extracost_k$: Extra cost per megawatt for operating generator type $k$ above the minimum level.
  \item $startcost_k$: Cost of starting up generator type $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
  \item $numon_{k,t}$: Number of generators of type $k$ that are on during period $t$.
  \item $level_{k,t}$: Level of electricity produced by generators of type $k$ during period $t$.
  \item $start_k$: Binary variable indicating whether generator type $k$ is started (1) or not (0).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + startcost_k \cdot start_k + extracost_k \cdot (level_{k,t} - minlevel_k) \cdot numon_{k,t} \right)
\]

\subsection*{Constraints}
\begin{align}
  \sum_{k=1}^{K} level_{k,t} & = demand_t, \quad \forall t \in T \tag{Demand Constraint} \\
  minlevel_k \cdot numon_{k,t} & \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k \in K, \forall t \in T \tag{Generator Operating Levels} \\
  numon_{k,t} & \leq num_k, \quad \forall k \in K, \forall t \in T \tag{Availability of Generators} \\
  start_k & \geq numon_{k,t} - numon_{k,t-1}, \quad \forall k \in K, t \in T \setminus \{1\} \tag{Startup Constraint}
\end{align}

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

\section*{Mathematical Model}

\subsection*{Sets}
\begin{itemize}
  \item $T$: Set of time periods in a day, $t = 1, \ldots, T$.
  \item $K$: Set of generator types, $k = 1, \ldots, K$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
  \item $demand_t$: Electricity demand during period $t$.
  \item $num_k$: Number of available generators of type $k$.
  \item $minlevel_k$: Minimum operating level of generator type $k$.
  \item $maxlevel_k$: Maximum operating level of generator type $k$.
  \item $runcost_k$: Hourly cost of running each generator of type $k$ at minimum level.
  \item $extracost_k$: Extra cost per megawatt for operating generator type $k$ above the minimum level.
  \item $startcost_k$: Cost of starting up generator type $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
  \item $numon_{k,t}$: Number of generators of type $k$ that are on during period $t$.
  \item $level_{k,t}$: Level of electricity produced by generators of type $k$ during period $t$.
  \item $start_k$: Binary variable indicating whether generator type $k$ is started (1) or not (0).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + startcost_k \cdot start_k + extracost_k \cdot (level_{k,t} - minlevel_k) \cdot numon_{k,t} \right)
\]

\subsection*{Constraints}
\begin{align}
  \sum_{k=1}^{K} level_{k,t} & = demand_t, \quad \forall t \in T \tag{Demand Constraint} \\
  minlevel_k \cdot numon_{k,t} & \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k \in K, \forall t \in T \tag{Generator Operating Levels} \\
  numon_{k,t} & \leq num_k, \quad \forall k \in K, \forall t \in T \tag{Availability of Generators} \\
  start_k & \geq numon_{k,t} - numon_{k,t-1}, \quad \forall k \in K, t \in T \setminus \{1\} \tag{Startup Constraint}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input in JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

#### Sets
T = len(data['demand'])  #### Number of time periods
K = len(data['num'])      #### Number of generator types

#### Parameters
demand = data['demand']
num_k = data['num']
minlevel_k = data['minlevel']
maxlevel_k = data['maxlevel']
runcost_k = data['runcost']
extracost_k = data['extracost']
startcost_k = data['startcost']

#### Decision Variables
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0)
start = pulp.LpVariable.dicts("start", range(K), cat='Binary')

#### Objective Function
problem += pulp.lpSum(runcost_k[k] * numon[k][t] + startcost_k[k] * start[k] +
                       extracost_k[k] * (level[k][t] - minlevel_k[k]) * numon[k][t]
                       for k in range(K) for t in range(T)), "Total_Cost"

#### Constraints
#### Demand Constraint
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == demand[t], f"Demand_Constraint_{t+1}"

#### Generator Operating Levels
for k in range(K):
    for t in range(T):
        problem += minlevel_k[k] * numon[k][t] <= level[k][t], f"Min_Operating_Level_{k+1}_{t+1}"
        problem += level[k][t] <= maxlevel_k[k] * numon[k][t], f"Max_Operating_Level_{k+1}_{t+1}"

#### Availability of Generators
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num_k[k], f"Availability_{k+1}_{t+1}"

#### Startup Constraint
for k in range(K):
    for t in range(1, T):  #### Start from 2nd time period
        problem += start[k] >= numon[k][t] - numon[k][t-1], f"Startup_Constraint_{k+1}_{t+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

