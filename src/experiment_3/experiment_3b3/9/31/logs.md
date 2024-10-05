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

\section*{Mathematical Model for Electricity Demand Management}

\subsection*{Indices}
\begin{itemize}
    \item \( t \): index representing time periods (1 to \( T \))
    \item \( k \): index representing generator types (1 to \( K \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( demand_t \): electricity demand at time \( t \)
    \item \( num_k \): number of available generators of type \( k \)
    \item \( minlevel_k \): minimum operational level for type \( k \)
    \item \( maxlevel_k \): maximum operational level for type \( k \)
    \item \( runcost_k \): cost of running type \( k \) generator at minimum level
    \item \( extracost_k \): extra cost per megawatt above minimum level for type \( k \)
    \item \( startcost_k \): startup cost for type \( k \) generator
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( numon_{k,t} \): number of generators of type \( k \) that are on at time \( t \)
    \item \( level_{k,t} \): operating level of type \( k \) generator at time \( t \) (above minimum)
    \item \( start_{k,t} \): binary variable indicating if type \( k \) generator is started at time \( t \) (1 if started, 0 otherwise)
\end{itemize}

\subsection*{Objective Function}
Minimize total cost \( C \):
\[
C = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot level_{k,t} + startcost_k \cdot start_{k,t} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:}
    \[
    \sum_{k=1}^{K} numon_{k,t} \cdot minlevel_k + \sum_{k=1}^{K} level_{k,t} \geq demand_t, \quad \forall t
    \]
    
    \item \textbf{Generator Capacity:}
    \[
    numon_{k,t} \cdot minlevel_k \leq \sum_{j=1}^{K} level_{j,t} \leq numon_{k,t} \cdot maxlevel_k, \quad \forall k, \forall t
    \]

    \item \textbf{Startup Decisions:}
    \[
    start_{k,t} \leq numon_{k,t}, \quad \forall k, \forall t
    \]
    
    \item \textbf{Availability of Generators:}
    \[
    numon_{k,t} \leq num_k, \quad \forall k, \forall t
    \]

    \item \textbf{Non-negativity:}
    \[
    numon_{k,t} \geq 0, \quad \forall k, \forall t
    \]
    
\end{itemize}

\subsection*{Output}
The output will be the variable \( numon \):
\[
\text{numon} = \left[ \left[ numon_{k,t} \, | \, t=1,\ldots,T \right] \, | \, k=1,\ldots,K \right]
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

\section*{Mathematical Model for Electricity Demand Management}

\subsection*{Indices}
\begin{itemize}
    \item \( t \): index representing time periods (1 to \( T \))
    \item \( k \): index representing generator types (1 to \( K \))
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( demand_t \): electricity demand at time \( t \)
    \item \( num_k \): number of available generators of type \( k \)
    \item \( minlevel_k \): minimum operational level for type \( k \)
    \item \( maxlevel_k \): maximum operational level for type \( k \)
    \item \( runcost_k \): cost of running type \( k \) generator at minimum level
    \item \( extracost_k \): extra cost per megawatt above minimum level for type \( k \)
    \item \( startcost_k \): startup cost for type \( k \) generator
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( numon_{k,t} \): number of generators of type \( k \) that are on at time \( t \)
    \item \( level_{k,t} \): operating level of type \( k \) generator at time \( t \) (above minimum)
    \item \( start_{k,t} \): binary variable indicating if type \( k \) generator is started at time \( t \) (1 if started, 0 otherwise)
\end{itemize}

\subsection*{Objective Function}
Minimize total cost \( C \):
\[
C = \sum_{t=1}^{T} \sum_{k=1}^{K} \left( runcost_k \cdot numon_{k,t} + extracost_k \cdot level_{k,t} + startcost_k \cdot start_{k,t} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Demand Satisfaction:}
    \[
    \sum_{k=1}^{K} numon_{k,t} \cdot minlevel_k + \sum_{k=1}^{K} level_{k,t} \geq demand_t, \quad \forall t
    \]
    
    \item \textbf{Generator Capacity:}
    \[
    numon_{k,t} \cdot minlevel_k \leq \sum_{j=1}^{K} level_{j,t} \leq numon_{k,t} \cdot maxlevel_k, \quad \forall k, \forall t
    \]

    \item \textbf{Startup Decisions:}
    \[
    start_{k,t} \leq numon_{k,t}, \quad \forall k, \forall t
    \]
    
    \item \textbf{Availability of Generators:}
    \[
    numon_{k,t} \leq num_k, \quad \forall k, \forall t
    \]

    \item \textbf{Non-negativity:}
    \[
    numon_{k,t} \geq 0, \quad \forall k, \forall t
    \]
    
\end{itemize}

\subsection*{Output}
The output will be the variable \( numon \):
\[
\text{numon} = \left[ \left[ numon_{k,t} \, | \, t=1,\ldots,T \right] \, | \, k=1,\ldots,K \right]
\]

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

#### Problem
problem = pulp.LpProblem("Electricity_Demand_Management", pulp.LpMinimize)

#### Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] + 
                      data['extracost'][k] * level[k, t] +
                      data['startcost'][k] * start[k, t] 
                      for k in range(K) for t in range(T))

#### Constraints
#### Demand Satisfaction
for t in range(T):
    problem += (pulp.lpSum(numon[k, t] * data['minlevel'][k] + level[k, t] for k in range(K)) >= data['demand'][t])

#### Generator Capacity
for k in range(K):
    for t in range(T):
        problem += (numon[k, t] * data['minlevel'][k] <= level[k, t])
        problem += (level[k, t] <= numon[k, t] * data['maxlevel'][k])

#### Startup Decisions
for k in range(K):
    for t in range(T):
        problem += (start[k, t] <= numon[k, t])

#### Availability of Generators
for k in range(K):
    for t in range(T):
        problem += (numon[k, t] <= data['num'][k])

#### Solve the problem
problem.solve()

#### Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

