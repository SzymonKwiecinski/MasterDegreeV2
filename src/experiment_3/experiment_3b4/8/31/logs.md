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
To model this problem, we will use a Mixed-Integer Programming (MIP) approach. We will define our decision variables, objective function, and constraints as follows:

**Decision Variables:**
- \( y_{k,t} \): Binary variable that is 1 if at least one unit of type \( k \) is started up in period \( t \), and 0 otherwise.
- \( numon_{k,t} \): Number of units of type \( k \) that are on in period \( t \).
- \( level_{k,t} \): The total megawatt output above the minimum level for all units of type \( k \) in period \( t \).

**Objective Function:**
Minimize the total cost, including running costs, extra costs, and start-up costs over all periods.

**Constraints:**
1. Demand must be met in each period.
2. Number of operating units of each type must not exceed available units.
3. Output level constraints for each type of generator.
4. Linking constraints between \( y_{k,t} \) and \( numon_{k,t} \) to account for the start-up costs.
5. Non-negativity and binary constraints as appropriate.

Below is the mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Mixed-Integer Programming Model for Power Station Scheduling}
\date{}
\maketitle

\section*{Decision Variables}
\begin{align*}
    & y_{k,t} \in \{0, 1\} && \text{1 if type \( k \) generator is started in period \( t \), 0 otherwise} \\
    & numon_{k,t} \in \mathbb{Z}^+ && \text{Number of type \( k \) generators on in period \( t \)} \\
    & level_{k,t} \geq 0 && \text{Total output above minimum for type \( k \) generators in period \( t \)}
\end{align*}

\section*{Objective Function}
Minimize the total cost:
\begin{align*}
    \min \sum_{t=1}^{T} \sum_{k=1}^{K} \Bigg( numon_{k,t} \cdot runcost_k + level_{k,t} \cdot extracost_k + y_{k,t} \cdot startcost_k \Bigg)
\end{align*}

\section*{Constraints}
\subsection*{Demand Fulfillment}
\begin{align*}
    \sum_{k=1}^{K} \left( numon_{k,t} \cdot minlevel_k + level_{k,t} \right) \geq demand_t, \quad \forall t = 1, \ldots, T
\end{align*}

\subsection*{Generator Limits}
\begin{align*}
    0 \leq numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\end{align*}

\subsection*{Output Level Constraints}
\begin{align*}
    0 \leq level_{k,t} \leq (maxlevel_k - minlevel_k) \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\end{align*}

\subsection*{Start-up Constraints}
\begin{align*}
    numon_{k,t} \leq numon_{k,t-1} + y_{k,t} \cdot num_k, \quad \forall k = 1, \ldots, K, \forall t = 2, \ldots, T
\end{align*}

\subsection*{Initial Condition}
\begin{align*}
    numon_{k,1} \leq y_{k,1} \cdot num_k, \quad \forall k = 1, \ldots, K
\end{align*}

\section*{Variable Domains}
\begin{align*}
    & y_{k,t} \in \{0, 1\}, \quad numon_{k,t} \in \mathbb{Z}^+, \quad level_{k,t} \geq 0
\end{align*}

\end{document}
```

This formulation captures the problem requirements, minimizing the total cost while ensuring demand satisfaction and operational constraints of the generators.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Mixed-Integer Programming Model for Power Station Scheduling}
\date{}
\maketitle

\section*{Decision Variables}
\begin{align*}
    & y_{k,t} \in \{0, 1\} && \text{1 if type \( k \) generator is started in period \( t \), 0 otherwise} \\
    & numon_{k,t} \in \mathbb{Z}^+ && \text{Number of type \( k \) generators on in period \( t \)} \\
    & level_{k,t} \geq 0 && \text{Total output above minimum for type \( k \) generators in period \( t \)}
\end{align*}

\section*{Objective Function}
Minimize the total cost:
\begin{align*}
    \min \sum_{t=1}^{T} \sum_{k=1}^{K} \Bigg( numon_{k,t} \cdot runcost_k + level_{k,t} \cdot extracost_k + y_{k,t} \cdot startcost_k \Bigg)
\end{align*}

\section*{Constraints}
\subsection*{Demand Fulfillment}
\begin{align*}
    \sum_{k=1}^{K} \left( numon_{k,t} \cdot minlevel_k + level_{k,t} \right) \geq demand_t, \quad \forall t = 1, \ldots, T
\end{align*}

\subsection*{Generator Limits}
\begin{align*}
    0 \leq numon_{k,t} \leq num_k, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\end{align*}

\subsection*{Output Level Constraints}
\begin{align*}
    0 \leq level_{k,t} \leq (maxlevel_k - minlevel_k) \cdot numon_{k,t}, \quad \forall k = 1, \ldots, K, \forall t = 1, \ldots, T
\end{align*}

\subsection*{Start-up Constraints}
\begin{align*}
    numon_{k,t} \leq numon_{k,t-1} + y_{k,t} \cdot num_k, \quad \forall k = 1, \ldots, K, \forall t = 2, \ldots, T
\end{align*}

\subsection*{Initial Condition}
\begin{align*}
    numon_{k,1} \leq y_{k,1} \cdot num_k, \quad \forall k = 1, \ldots, K
\end{align*}

\section*{Variable Domains}
\begin{align*}
    & y_{k,t} \in \{0, 1\}, \quad numon_{k,t} \in \mathbb{Z}^+, \quad level_{k,t} \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])
K = len(data['num'])

#### Initialize the problem
problem = pulp.LpProblem("Power_Station_Scheduling", pulp.LpMinimize)

#### Decision variables
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), 0, 1, pulp.LpBinary)
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpInteger)
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpContinuous)

#### Objective function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] + level[k, t] * data['extracost'][k] + y[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

#### Constraints

#### Demand Fulfillment
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + level[k, t]
        for k in range(K)
    ) >= data['demand'][t]

#### Generator Limits
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

#### Output Level Constraints
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * numon[k, t]

#### Start-up Constraints
for k in range(K):
    for t in range(1, T):
        problem += numon[k, t] <= numon[k, t-1] + y[k, t] * data['num'][k]

#### Initial Condition
for k in range(K):
    problem += numon[k, 0] <= y[k, 0] * data['num'][k]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

