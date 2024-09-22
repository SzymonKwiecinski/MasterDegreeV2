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
    \item $T$: Number of time periods in a day
    \item $K$: Number of generator types
    \item $demand_t$: Demand for electricity in period $t$, $t = 1, \ldots, T$
    \item $num_k$: Number of generators of type $k$, $k = 1, \ldots, K$
    \item $minlevel_k$: Minimum operational level of generator type $k$
    \item $maxlevel_k$: Maximum operational level of generator type $k$
    \item $runcost_k$: Hourly cost of running each type $k$ generator at minimum level
    \item $extracost_k$: Extra hourly cost per megawatt for type $k$ generator operated above minimum level
    \item $startcost_k$: Startup cost for generator type $k$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $numon_{k,t}$: Number of type $k$ generators on in period $t$
    \item $level_{k,t}$: Operational level of type $k$ generator in period $t$ (in megawatts)
    \item $startup_{k,t}$: Binary variable indicating if type $k$ generator is started up in period $t$
\end{itemize}

\subsection*{Objective Function}

The goal is to minimize the total cost, which includes running costs, extra costs for exceeding minimum levels, and startup costs:

\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot (level_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot startup_{k,t} \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Demand Satisfaction:}
    \[
    \sum_{k=1}^{K} level_{k,t} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Operational Level Limits:}
    \[
    minlevel_k \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]

    \item \textbf{Generator Availability:}
    \[
    \sum_{t=1}^{T} numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K
    \]

    \item \textbf{Startup Decision:}
    \[
    level_{k,t} \leq maxlevel_k \cdot startup_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]

    \item \textbf{Binary Variable Constraints:}
    \[
    startup_{k,t} \in \{0, 1\}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]
\end{itemize}

\subsection*{Output}

The output will consist of the number of generators of each type that are on in each period:

\[
\text{Output: } \{ numon: [[numon_{k,t} \text{ for } t = 1, \ldots, T] \text{ for } k = 1, \ldots, K] ] \}
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
    \item $T$: Number of time periods in a day
    \item $K$: Number of generator types
    \item $demand_t$: Demand for electricity in period $t$, $t = 1, \ldots, T$
    \item $num_k$: Number of generators of type $k$, $k = 1, \ldots, K$
    \item $minlevel_k$: Minimum operational level of generator type $k$
    \item $maxlevel_k$: Maximum operational level of generator type $k$
    \item $runcost_k$: Hourly cost of running each type $k$ generator at minimum level
    \item $extracost_k$: Extra hourly cost per megawatt for type $k$ generator operated above minimum level
    \item $startcost_k$: Startup cost for generator type $k$
\end{itemize}

\subsection*{Decision Variables}

\begin{itemize}
    \item $numon_{k,t}$: Number of type $k$ generators on in period $t$
    \item $level_{k,t}$: Operational level of type $k$ generator in period $t$ (in megawatts)
    \item $startup_{k,t}$: Binary variable indicating if type $k$ generator is started up in period $t$
\end{itemize}

\subsection*{Objective Function}

The goal is to minimize the total cost, which includes running costs, extra costs for exceeding minimum levels, and startup costs:

\[
\text{Minimize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot (level_{k,t} - minlevel_k) \cdot numon_{k,t} + startcost_k \cdot startup_{k,t} \right)
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Demand Satisfaction:}
    \[
    \sum_{k=1}^{K} level_{k,t} \geq demand_t, \quad \forall t = 1, \ldots, T
    \]

    \item \textbf{Operational Level Limits:}
    \[
    minlevel_k \cdot numon_{k,t} \leq level_{k,t} \leq maxlevel_k \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]

    \item \textbf{Generator Availability:}
    \[
    \sum_{t=1}^{T} numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K
    \]

    \item \textbf{Startup Decision:}
    \[
    level_{k,t} \leq maxlevel_k \cdot startup_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]

    \item \textbf{Binary Variable Constraints:}
    \[
    startup_{k,t} \in \{0, 1\}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
    \]
\end{itemize}

\subsection*{Output}

The output will consist of the number of generators of each type that are on in each period:

\[
\text{Output: } \{ numon: [[numon_{k,t} \text{ for } t = 1, \ldots, T] \text{ for } k = 1, \ldots, K] ] \}
\]

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])  #### Number of time periods
K = len(data['num'])      #### Number of generator types

#### Define the problem
problem = pulp.LpProblem("PowerGenerationOptimization", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpInteger)
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), 0, None)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), 0, 1, pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t] +
    data['startcost'][k] * startup[k, t]
    for k in range(K) for t in range(T)
)

#### Constraints
#### Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) >= data['demand'][t]

#### Operational Level Limits
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

#### Generator Availability
for k in range(K):
    problem += pulp.lpSum(numon[k, t] for t in range(T)) <= data['num'][k]

#### Startup Decision
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= data['maxlevel'][k] * startup[k, t]

#### Solve the problem
problem.solve()

#### Output the results
numon_output = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

