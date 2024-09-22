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

\section*{Mathematical Model for Power Generation Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of time periods in a day.
    \item $K$: Number of types of generating units.
    \item $demand_t$: Electricity demand at time period $t$, where $t = 1, \ldots, T$.
    \item $num_k$: Number of units for type $k$, where $k = 1, \ldots, K$.
    \item $minlevel_k$: Minimum operational level of type $k$.
    \item $maxlevel_k$: Maximum operational level of type $k$.
    \item $runcost_k$: Hourly cost of running type $k$ generator at minimum level.
    \item $extracost_k$: Additional cost per megawatt for type $k$ above minimum level.
    \item $startcost_k$: Startup cost for type $k$ generator.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on during period $t$.
    \item $power_{k,t}$: Power output of type $k$ generator during period $t$.
    \item $startup_{k,t}$: Binary variable indicating if type $k$ generator is started during period $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot (power_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot startup_{k,t} \right)
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Demand satisfaction:
    \[
    \sum_{k=1}^{K} power_{k,t} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item Power output limits for each generator type:
    \[
    minlevel_k \cdot numon_{k,t} \leq power_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Binary startup variable:
    \[
    power_{k,t} \leq maxlevel_k \cdot startup_{k,t}, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Number of units on limits:
    \[
    numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Non-negativity constraints:
    \[
    numon_{k,t} \geq 0, \quad power_{k,t} \geq 0, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

\end{enumerate}

\subsection*{Output}
The output will consist of a matrix $numon$ where each element represents the number of generators of type $k$ that are on during time period $t$:
\[
\text{Output: } 
numon = \left[ [numon_{k, t} \text{ for } t = 1, \ldots, T] \text{ for } k = 1, \ldots, K] \right]
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

\section*{Mathematical Model for Power Generation Optimization}

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of time periods in a day.
    \item $K$: Number of types of generating units.
    \item $demand_t$: Electricity demand at time period $t$, where $t = 1, \ldots, T$.
    \item $num_k$: Number of units for type $k$, where $k = 1, \ldots, K$.
    \item $minlevel_k$: Minimum operational level of type $k$.
    \item $maxlevel_k$: Maximum operational level of type $k$.
    \item $runcost_k$: Hourly cost of running type $k$ generator at minimum level.
    \item $extracost_k$: Additional cost per megawatt for type $k$ above minimum level.
    \item $startcost_k$: Startup cost for type $k$ generator.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $numon_{k,t}$: Number of generators of type $k$ that are on during period $t$.
    \item $power_{k,t}$: Power output of type $k$ generator during period $t$.
    \item $startup_{k,t}$: Binary variable indicating if type $k$ generator is started during period $t$.
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot (power_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot startup_{k,t} \right)
\]

\subsection*{Constraints}

\begin{enumerate}
    \item Demand satisfaction:
    \[
    \sum_{k=1}^{K} power_{k,t} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item Power output limits for each generator type:
    \[
    minlevel_k \cdot numon_{k,t} \leq power_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Binary startup variable:
    \[
    power_{k,t} \leq maxlevel_k \cdot startup_{k,t}, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Number of units on limits:
    \[
    numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

    \item Non-negativity constraints:
    \[
    numon_{k,t} \geq 0, \quad power_{k,t} \geq 0, \quad \forall k = 1, \ldots, K, \quad \forall t = 1, \ldots, T
    \]

\end{enumerate}

\subsection*{Output}
The output will consist of a matrix $numon$ where each element represents the number of generators of type $k$ that are on during time period $t$:
\[
\text{Output: } 
numon = \left[ [numon_{k, t} \text{ for } t = 1, \ldots, T] \text{ for } k = 1, \ldots, K] \right]
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

#### Define parameters
T = len(data['demand'])            #### Number of time periods
K = len(data['num'])                #### Number of types of generating units

#### Create the problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

#### Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), cat='Binary')

#### Objective function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                      data['extracost'][k] * (power[k][t] - data['minlevel'][k]) * numon[k][t] +
                      data['startcost'][k] * startup[k][t]
                      for k in range(K) for t in range(T))

#### Constraints
#### Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= data['demand'][t]

#### Power output limits for each generator type
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= power[k][t]
        problem += power[k][t] <= data['maxlevel'][k] * numon[k][t]

#### Binary startup variable
for k in range(K):
    for t in range(T):
        problem += power[k][t] <= data['maxlevel'][k] * startup[k][t]

#### Number of units on limits
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

#### Solve the problem
problem.solve()

#### Output the number of generators on
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

print(f'Number of Generators On: {numon_output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

