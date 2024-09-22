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
To formulate the given problem as a Mixed Integer Programming (MIP) model, we need to define the decision variables, the objective function, and the constraints clearly. Below is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Electricity Load Demand Optimization}
\author{}
\date{}
\maketitle

\section{Problem Formulation}

\subsection{Sets and Indices}
\begin{itemize}
    \item $T$: Set of time periods, indexed by $t = 1, \ldots, T$.
    \item $K$: Set of generator types, indexed by $k = 1, \ldots, K$.
\end{itemize}

\subsection{Parameters}
\begin{itemize}
    \item $demand_t$: Electricity demand in period $t$.
    \item $num_k$: Number of available units of generator type $k$.
    \item $minlevel_k$: Minimum operating level of generator type $k$.
    \item $maxlevel_k$: Maximum operating level of generator type $k$.
    \item $runcost_k$: Cost of running a generator type $k$ at the minimum level.
    \item $extracost_k$: Additional cost for each MW above the minimum level for generator type $k$.
    \item $startcost_k$: Cost of starting a generator type $k$.
\end{itemize}

\subsection{Decision Variables}
\begin{itemize}
    \item $numon_{k,t} \in \{0, 1, \ldots, num_k\}$: Number of generators of type $k$ running in period $t$.
    \item $power_{k,t} \geq 0$: Power output of all generators of type $k$ during period $t$.
    \item $start_{k,t} \in \{0, 1\}$: Binary variable indicating if a generator of type $k$ is started in period $t$.
\end{itemize}

\subsection{Objective Function}
The objective is to minimize the total cost, which comprises the running cost, extra cost for power above the minimum level, and the starting cost. 

\begin{align}
\text{Minimize } & \sum_{t=1}^{T} \sum_{k=1}^{K} \big[ runcost_k \cdot numon_{k,t} + extracost_k \cdot (power_{k,t} - numon_{k,t} \cdot minlevel_k) \big] \\
& + \sum_{t=1}^{T} \sum_{k=1}^{K} startcost_k \cdot start_{k,t}
\end{align}

\subsection{Constraints}
\begin{align}
& \sum_{k=1}^{K} power_{k,t} \geq demand_t, \quad \forall t \\

& numon_{k,t} \cdot minlevel_k \leq power_{k,t} \leq numon_{k,t} \cdot maxlevel_k, \quad \forall k, \forall t \\

& start_{k,t} \geq numon_{k,t} - numon_{k,t-1}, \quad \forall k, \forall t \text{ with } t \geq 2 \\

& 0 \leq numon_{k,t} \leq num_k, \quad \forall k, \forall t \\

& start_{k,t} \in \{0, 1\}, \quad \forall k, \forall t
\end{align}

\end{document}
```

This model helps in determining which generators should be operating during each period of the day to minimize the total cost while satisfying the electricity demand and operational constraints of each generator type. The binary variable `start_{k,t}` ensures that the start-up costs are considered only when a generator is turned on. The objective function captures the cost associated with running the generators at or beyond the minimum level and any associated start-up costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Electricity Load Demand Optimization}
\author{}
\date{}
\maketitle

\section{Problem Formulation}

\subsection{Sets and Indices}
\begin{itemize}
    \item $T$: Set of time periods, indexed by $t = 1, \ldots, T$.
    \item $K$: Set of generator types, indexed by $k = 1, \ldots, K$.
\end{itemize}

\subsection{Parameters}
\begin{itemize}
    \item $demand_t$: Electricity demand in period $t$.
    \item $num_k$: Number of available units of generator type $k$.
    \item $minlevel_k$: Minimum operating level of generator type $k$.
    \item $maxlevel_k$: Maximum operating level of generator type $k$.
    \item $runcost_k$: Cost of running a generator type $k$ at the minimum level.
    \item $extracost_k$: Additional cost for each MW above the minimum level for generator type $k$.
    \item $startcost_k$: Cost of starting a generator type $k$.
\end{itemize}

\subsection{Decision Variables}
\begin{itemize}
    \item $numon_{k,t} \in \{0, 1, \ldots, num_k\}$: Number of generators of type $k$ running in period $t$.
    \item $power_{k,t} \geq 0$: Power output of all generators of type $k$ during period $t$.
    \item $start_{k,t} \in \{0, 1\}$: Binary variable indicating if a generator of type $k$ is started in period $t$.
\end{itemize}

\subsection{Objective Function}
The objective is to minimize the total cost, which comprises the running cost, extra cost for power above the minimum level, and the starting cost. 

\begin{align}
\text{Minimize } & \sum_{t=1}^{T} \sum_{k=1}^{K} \big[ runcost_k \cdot numon_{k,t} + extracost_k \cdot (power_{k,t} - numon_{k,t} \cdot minlevel_k) \big] \\
& + \sum_{t=1}^{T} \sum_{k=1}^{K} startcost_k \cdot start_{k,t}
\end{align}

\subsection{Constraints}
\begin{align}
& \sum_{k=1}^{K} power_{k,t} \geq demand_t, \quad \forall t \\

& numon_{k,t} \cdot minlevel_k \leq power_{k,t} \leq numon_{k,t} \cdot maxlevel_k, \quad \forall k, \forall t \\

& start_{k,t} \geq numon_{k,t} - numon_{k,t-1}, \quad \forall k, \forall t \text{ with } t \geq 2 \\

& 0 \leq numon_{k,t} \leq num_k, \quad \forall k, \forall t \\

& start_{k,t} \in \{0, 1\}, \quad \forall k, \forall t
\end{align}

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

#### Define sets and parameters
T = len(data['demand'])
K = len(data['num'])
demand_t = data['demand']
num_k = data['num']
minlevel_k = data['minlevel']
maxlevel_k = data['maxlevel']
runcost_k = data['runcost']
extracost_k = data['extracost']
startcost_k = data['startcost']

#### Create the problem
problem = pulp.LpProblem("Electricity_Load_Demand_Optimization", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), 0, None, pulp.LpInteger)
power = pulp.LpVariable.dicts("power", (range(K), range(T)), 0)
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(
    runcost_k[k] * numon[k][t] + 
    extracost_k[k] * (power[k][t] - numon[k][t] * minlevel_k[k]) 
    for k in range(K) for t in range(T)
) + pulp.lpSum(startcost_k[k] * start[k][t] for k in range(K) for t in range(T))

#### Constraints
for t in range(T):
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= demand_t[t], f"demand_constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += numon[k][t] * minlevel_k[k] <= power[k][t], f"min_power_constraint_{k}_{t}"
        problem += power[k][t] <= numon[k][t] * maxlevel_k[k], f"max_power_constraint_{k}_{t}"

for k in range(K):
    for t in range(1, T):
        problem += start[k][t] >= numon[k][t] - numon[k][t-1], f"start_constraint_{k}_{t}"

for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num_k[k], f"capacity_constraint_{k}_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

