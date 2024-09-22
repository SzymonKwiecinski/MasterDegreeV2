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

\section*{Mathematical Model for Generator Scheduling Problem}

\subsection*{Parameters}

\begin{itemize}
    \item $T$: Total number of time periods in a day.
    \item $K$: Total number of generator types.
    \item $demand_{t}$: Demand for electricity at period $t$, for $t = 1,\ldots,T$.
    \item $num_{k}$: Number of generators of type $k$, for $k = 1,\ldots,K$.
    \item $minlevel_{k}$: Minimum operational level of generator type $k$, for $k = 1,\ldots,K$.
    \item $maxlevel_{k}$: Maximum operational level of generator type $k$, for $k = 1,\ldots,K$.
    \item $runcost_{k}$: Cost of running generator type $k$ at minimum level per hour, for $k = 1,\ldots,K$.
    \item $extracost_{k}$: Extra cost per megawatt for exceeding the minimum level of generator type $k$, for $k = 1,\ldots,K$.
    \item $startcost_{k}$: Startup cost for generator type $k$, for $k = 1,\ldots,K$.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on at period $t$, for $k = 1,\ldots,K$ and $t = 1,\ldots,T$.
    \item $level_{k,t}$: Operational level of generator type $k$ at period $t$, for $k = 1,\ldots,K$ and $t = 1,\ldots,T$.
    \item $is\_on_{k,t}$: Binary variable indicating if generator type $k$ is turned on at period $t$ ($1$ if on, $0$ if off).
\end{itemize}

\subsection*{Objective Function}

Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_{k} \cdot numon_{k,t} + extracost_{k} \cdot (level_{k,t} - minlevel_{k}) \cdot numon_{k,t} + startcost_{k} \cdot is\_on_{k,t} \right)
\]

\subsection*{Constraints}

1. Demand satisfaction:
\[
\sum_{k=1}^{K} level_{k,t} \geq demand_{t}, \quad \forall t = 1,\ldots,T
\]

2. Operational level bounds:
\[
minlevel_{k} \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_{k} \cdot numon_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

3. Generators on/off:
\[
level_{k,t} \leq maxlevel_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

4. Minimum level enforcement:
\[
level_{k,t} \geq minlevel_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

5. Number of generators:
\[
numon_{k,t} \leq num_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
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

\section*{Mathematical Model for Generator Scheduling Problem}

\subsection*{Parameters}

\begin{itemize}
    \item $T$: Total number of time periods in a day.
    \item $K$: Total number of generator types.
    \item $demand_{t}$: Demand for electricity at period $t$, for $t = 1,\ldots,T$.
    \item $num_{k}$: Number of generators of type $k$, for $k = 1,\ldots,K$.
    \item $minlevel_{k}$: Minimum operational level of generator type $k$, for $k = 1,\ldots,K$.
    \item $maxlevel_{k}$: Maximum operational level of generator type $k$, for $k = 1,\ldots,K$.
    \item $runcost_{k}$: Cost of running generator type $k$ at minimum level per hour, for $k = 1,\ldots,K$.
    \item $extracost_{k}$: Extra cost per megawatt for exceeding the minimum level of generator type $k$, for $k = 1,\ldots,K$.
    \item $startcost_{k}$: Startup cost for generator type $k$, for $k = 1,\ldots,K$.
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on at period $t$, for $k = 1,\ldots,K$ and $t = 1,\ldots,T$.
    \item $level_{k,t}$: Operational level of generator type $k$ at period $t$, for $k = 1,\ldots,K$ and $t = 1,\ldots,T$.
    \item $is\_on_{k,t}$: Binary variable indicating if generator type $k$ is turned on at period $t$ ($1$ if on, $0$ if off).
\end{itemize}

\subsection*{Objective Function}

Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_{k} \cdot numon_{k,t} + extracost_{k} \cdot (level_{k,t} - minlevel_{k}) \cdot numon_{k,t} + startcost_{k} \cdot is\_on_{k,t} \right)
\]

\subsection*{Constraints}

1. Demand satisfaction:
\[
\sum_{k=1}^{K} level_{k,t} \geq demand_{t}, \quad \forall t = 1,\ldots,T
\]

2. Operational level bounds:
\[
minlevel_{k} \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_{k} \cdot numon_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

3. Generators on/off:
\[
level_{k,t} \leq maxlevel_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

4. Minimum level enforcement:
\[
level_{k,t} \geq minlevel_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

5. Number of generators:
\[
numon_{k,t} \leq num_{k} \cdot is\_on_{k,t}, \quad \forall k = 1,\ldots,K, \forall t = 1,\ldots,T
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the given JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

#### Parameters
T = len(data['demand'])  #### Total number of time periods
K = len(data['num'])      #### Total number of generator types

#### Create the LP problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, upBound=None)
is_on = pulp.LpVariable.dicts("is_on", (range(K), range(T)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                       data['extracost'][k] * (level[k][t] - data['minlevel'][k]) * numon[k][t] +
                       data['startcost'][k] * is_on[k][t]
                       for k in range(K) for t in range(T))

#### Constraints
#### Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) >= data['demand'][t]

#### Operational level bounds
for k in range(K):
    for t in range(T):
        problem += level[k][t] >= data['minlevel'][k] * is_on[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * is_on[k][t]

#### Generators on/off
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= data['maxlevel'][k] * is_on[k][t]

#### Number of generators
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k] * is_on[k][t]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

