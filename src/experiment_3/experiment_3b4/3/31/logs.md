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
To model the problem as a Mixed Integer Programming (MIP) problem, we need to define decision variables, objective function, and constraints clearly. Here's the mathematical formulation:

Let:
- \( T \) be the number of periods in a day.
- \( K \) be the number of types of generators.

Decision Variables:
- \( \text{numon}_{k, t} \): Number of type \( k \) generators turned on in period \( t \).
- \( \text{level}_{k, t} \): Power level above minimum level for type \( k \) generators in period \( t \).

The decision variables for generator operation can be binary or continuous depending on whether we are considering the unit being on or the power level above minimum.

Objective Function:
The objective is to minimize the total cost, which includes the running cost, extra cost for power above minimum, and startup cost.

Constraints:
1. Meet demand in each period \( t \).
2. Generator operational limits.

Here's the formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{MIP Formulation for Power Generation}

\subsection*{Sets and Indices}
\begin{align*}
T & : \text{Number of periods in a day} \\
K & : \text{Number of generator types} \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{demand}_{t} & : \text{Electricity demand in period } t, \; t=1,\dots,T \\
\text{num}_{k} & : \text{Number of available generators of type } k, \; k=1,\dots,K \\
\text{minlevel}_{k} & : \text{Minimum generation level of type } k \\
\text{maxlevel}_{k} & : \text{Maximum generation level of type } k \\
\text{runcost}_{k} & : \text{Running cost at minimum level for type } k \\
\text{extracost}_{k} & : \text{Extra cost per MW above minimum for type } k \\
\text{startcost}_{k} & : \text{Startup cost for type } k \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{numon}_{k,t} & : \text{Number of generators of type } k \text{ that are on in period } t \\
\text{level}_{k,t} & : \text{Power level above minimum for generators of type } k \text{ in period } t \\
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\begin{align*}
\text{Minimize} \quad & \sum_{t=1}^{T} \sum_{k=1}^{K} \left( \text{numon}_{k,t} \cdot \text{runcost}_{k} + \text{level}_{k,t} \cdot \text{extracost}_{k} + \text{u}_{k,t} \cdot \text{startcost}_{k} \right)
\end{align*}
where \( \text{u}_{k,t} \) is a binary variable indicating if at least one generator of type \( k \) starts in period \( t \).

\subsection*{Constraints}

1. Meet demand in each period:
\begin{align*}
\sum_{k=1}^{K} \left( \text{numon}_{k,t} \cdot \text{minlevel}_{k} + \text{level}_{k,t} \right) & \geq \text{demand}_{t}, \quad \forall t=1,\dots,T
\end{align*}

2. Generator operational limits:
\begin{align*}
0 \leq \text{level}_{k,t} & \leq \text{numon}_{k,t} \cdot (\text{maxlevel}_{k} - \text{minlevel}_{k}), \quad \forall k=1,\dots,K, \; t=1,\dots,T \\
0 \leq \text{numon}_{k,t} & \leq \text{num}_{k}, \quad \forall k=1,\dots,K, \; t=1,\dots,T
\end{align*}

3. Binary start-up condition:
\begin{align*}
\text{u}_{k,t} \geq & \text{numon}_{k,t} - \text{numon}_{k,t-1}, \quad \forall k=1,\dots,K, \; t=1,\dots,T
\end{align*}

\end{document}
```

This model captures the key aspects of scheduling power generators to meet electricity demand while minimizing costs, including the cost of starting up, running at minimum level, and producing more than the minimum level of power. Constraints ensure that demand is met efficiently while adhering to operational limits.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\begin{document}

\section*{MIP Formulation for Power Generation}

\subsection*{Sets and Indices}
\begin{align*}
T & : \text{Number of periods in a day} \\
K & : \text{Number of generator types} \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
\text{demand}_{t} & : \text{Electricity demand in period } t, \; t=1,\dots,T \\
\text{num}_{k} & : \text{Number of available generators of type } k, \; k=1,\dots,K \\
\text{minlevel}_{k} & : \text{Minimum generation level of type } k \\
\text{maxlevel}_{k} & : \text{Maximum generation level of type } k \\
\text{runcost}_{k} & : \text{Running cost at minimum level for type } k \\
\text{extracost}_{k} & : \text{Extra cost per MW above minimum for type } k \\
\text{startcost}_{k} & : \text{Startup cost for type } k \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
\text{numon}_{k,t} & : \text{Number of generators of type } k \text{ that are on in period } t \\
\text{level}_{k,t} & : \text{Power level above minimum for generators of type } k \text{ in period } t \\
\end{align*}

\subsection*{Objective Function}
Minimize the total cost:
\begin{align*}
\text{Minimize} \quad & \sum_{t=1}^{T} \sum_{k=1}^{K} \left( \text{numon}_{k,t} \cdot \text{runcost}_{k} + \text{level}_{k,t} \cdot \text{extracost}_{k} + \text{u}_{k,t} \cdot \text{startcost}_{k} \right)
\end{align*}
where \( \text{u}_{k,t} \) is a binary variable indicating if at least one generator of type \( k \) starts in period \( t \).

\subsection*{Constraints}

1. Meet demand in each period:
\begin{align*}
\sum_{k=1}^{K} \left( \text{numon}_{k,t} \cdot \text{minlevel}_{k} + \text{level}_{k,t} \right) & \geq \text{demand}_{t}, \quad \forall t=1,\dots,T
\end{align*}

2. Generator operational limits:
\begin{align*}
0 \leq \text{level}_{k,t} & \leq \text{numon}_{k,t} \cdot (\text{maxlevel}_{k} - \text{minlevel}_{k}), \quad \forall k=1,\dots,K, \; t=1,\dots,T \\
0 \leq \text{numon}_{k,t} & \leq \text{num}_{k}, \quad \forall k=1,\dots,K, \; t=1,\dots,T
\end{align*}

3. Binary start-up condition:
\begin{align*}
\text{u}_{k,t} \geq & \text{numon}_{k,t} - \text{numon}_{k,t-1}, \quad \forall k=1,\dots,K, \; t=1,\dots,T
\end{align*}

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

T = len(data['demand'])
K = len(data['num'])

#### Define problem
problem = pulp.LpProblem("Power_Generation_Minimization", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("NumOn", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, upBound=None, cat=pulp.LpInteger)
level = pulp.LpVariable.dicts("Level", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, upBound=None, cat=pulp.LpContinuous)
u = pulp.LpVariable.dicts("U", ((k, t) for k in range(K) for t in range(T)), 
                          cat=pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] +
    level[k, t] * data['extracost'][k] +
    u[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

#### Constraints
#### Meet demand in each period
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + level[k, t]
        for k in range(K)
    ) >= data['demand'][t]

#### Generator operational limits
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= numon[k, t] * (data['maxlevel'][k] - data['minlevel'][k])
        problem += numon[k, t] <= data['num'][k]

#### Binary start-up condition
for k in range(K):
    for t in range(1, T):
        problem += u[k, t] >= numon[k, t] - numon[k, t - 1]
    #### Initial condition for t = 0
    problem += u[k, 0] >= numon[k, 0]

#### Solve problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

