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

\subsection*{Sets}
\begin{itemize}
    \item $T$: Set of time periods in a day, $t \in \{1, \ldots, T\}$
    \item $K$: Set of generator types, $k \in \{1, \ldots, K\}$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $demand_{t}$: Electricity demand at time period $t$ 
    \item $num_{k}$: Number of available generators of type $k$
    \item $minlevel_{k}$: Minimum operational level of generator type $k$
    \item $maxlevel_{k}$: Maximum operational level of generator type $k$
    \item $runcost_{k}$: Cost of operating generator type $k$ at minimum level
    \item $extracost_{k}$: Additional cost per megawatt for operating generator type $k$ above minimum level
    \item $startcost_{k}$: Starting cost for generator type $k$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on during time period $t$
    \item $level_{k,t}$: Operational level of generator type $k$ during time period $t$
    \item $y_{k,t}$: Binary variable indicating if generator type $k$ is on during time period $t$ (1 if on, 0 if off)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\begin{align*}
    \text{Minimize} \quad Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( startcost_{k} \cdot y_{k,t} + runcost_{k} \cdot numon_{k,t} + extracost_{k} \cdot (level_{k,t} - minlevel_{k}) \cdot numon_{k,t} \right)
\end{align*}

\subsection*{Constraints}

1. Demand satisfaction constraint:
\begin{align*}
    \sum_{k=1}^{K} level_{k,t} = demand_{t}, \quad \forall t \in T
\end{align*}

2. Operational level constraints:
\begin{align*}
    minlevel_{k} \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_{k} \cdot numon_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

3. Generator operational constraints:
\begin{align*}
    numon_{k,t} \leq num_{k} \cdot y_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

4. Binary constraints for startup:
\begin{align*}
    numon_{k,t} \leq num_{k} \cdot y_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

5. Non-negativity and binary variables:
\begin{align*}
    numon_{k,t} \geq 0, \quad \forall k \in K, \forall t \in T \\
    y_{k,t} \in \{0,1\}, \quad \forall k \in K, \forall t \in T
\end{align*}

\subsection*{Output}
The output will be:
\begin{align*}
    numon = \left[ [numon_{k,t}]_{t=1}^{T} \right]_{k=1}^{K}
\end{align*}

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

\subsection*{Sets}
\begin{itemize}
    \item $T$: Set of time periods in a day, $t \in \{1, \ldots, T\}$
    \item $K$: Set of generator types, $k \in \{1, \ldots, K\}$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $demand_{t}$: Electricity demand at time period $t$ 
    \item $num_{k}$: Number of available generators of type $k$
    \item $minlevel_{k}$: Minimum operational level of generator type $k$
    \item $maxlevel_{k}$: Maximum operational level of generator type $k$
    \item $runcost_{k}$: Cost of operating generator type $k$ at minimum level
    \item $extracost_{k}$: Additional cost per megawatt for operating generator type $k$ above minimum level
    \item $startcost_{k}$: Starting cost for generator type $k$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on during time period $t$
    \item $level_{k,t}$: Operational level of generator type $k$ during time period $t$
    \item $y_{k,t}$: Binary variable indicating if generator type $k$ is on during time period $t$ (1 if on, 0 if off)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\begin{align*}
    \text{Minimize} \quad Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( startcost_{k} \cdot y_{k,t} + runcost_{k} \cdot numon_{k,t} + extracost_{k} \cdot (level_{k,t} - minlevel_{k}) \cdot numon_{k,t} \right)
\end{align*}

\subsection*{Constraints}

1. Demand satisfaction constraint:
\begin{align*}
    \sum_{k=1}^{K} level_{k,t} = demand_{t}, \quad \forall t \in T
\end{align*}

2. Operational level constraints:
\begin{align*}
    minlevel_{k} \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_{k} \cdot numon_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

3. Generator operational constraints:
\begin{align*}
    numon_{k,t} \leq num_{k} \cdot y_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

4. Binary constraints for startup:
\begin{align*}
    numon_{k,t} \leq num_{k} \cdot y_{k,t}, \quad \forall k \in K, \forall t \in T
\end{align*}

5. Non-negativity and binary variables:
\begin{align*}
    numon_{k,t} \geq 0, \quad \forall k \in K, \forall t \in T \\
    y_{k,t} \in \{0,1\}, \quad \forall k \in K, \forall t \in T
\end{align*}

\subsection*{Output}
The output will be:
\begin{align*}
    numon = \left[ [numon_{k,t}]_{t=1}^{T} \right]_{k=1}^{K}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

#### Define model
T = len(data['demand'])
K = len(data['num'])
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(
    data['startcost'][k] * y[k, t] + 
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t] 
    for k in range(K) for t in range(T)
)

#### Constraints

#### Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) == data['demand'][t]

#### Operational level constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

#### Generator operational constraints
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k] * y[k, t]

#### Non-negativity and binary constraints (already handled in variable definitions)

#### Solve the problem
problem.solve()

#### Output the results
numon_output = [[pulp.value(numon[k, t]) for k in range(K)] for t in range(T)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

