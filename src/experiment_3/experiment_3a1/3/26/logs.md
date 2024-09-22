# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- An economy consists of several industries. 
- Each unit produced by one of the industries (a unit will be taken as £1’s worth of value of production) requires inputs from possibly its own industry as well as other industries. 
- Industry \var{k} requires \var{inputone_{k, j}} input from industy \var{j}.
- Industry \var{k} requires \var{manpowerone_{k}} units of manpower.
- There is a time lag in the economy so that the output in year t + 1 requires an input in year t.
- Output from an industry may also be used to build productive capacity for itself or other industries in future years.
- To give unit increases (capacity for £1’s worth of extra production) in productive capacity of industry \var{k}, \var{j} units of industry \var{inputtwo_{k, j}} and \var{manpowertwo{k}} units of manpower are needed.
- Input from an industry in year t results in a (permanent) increase in productive capacity in year t + 2.
- Stocks of goods may be held from year to year. 
- At present (year 0), the stocks of industry \var{k} is \var{stock_{k}}, and the capacity of industry \var{k} is \var{capacity_{k}}.
- An exogenous consumption requirement of \var{demand_{k}} units from industry \var{k} has to be satisfied in every year except year 0.


INPUT FORMAT:

{
    "inputone": [[inputone_{k, j} for j in 1,...,K] for k in 1,...,K],
    "manpowerone": [manpowerone_{k} for k in 1,...,K],
    "inputtwo": [[inputtwo_{k, j} for j in 1,...,K] for k in 1,...,K],
    "manpowertwo": [manpowertwo_{k} for k in 1,...,K],
    "stock": [stock_{k} for k in 1,...,K],
    "capacity": [capacity_{k} for k in 1,...,K],
    "demand": [demand_{k} for k in 1,...,K]
}


OBJECTIVE: Maximize the total manpower requirement over five years

OUTPUT INFO:

- \var{produce} represents the amount of units produced by each industry in each year
- \var{buildcapa} represents the amount of units used to build productive capacity for each industry in each year
- \var{stockhold} represents the amount of stock of each industry held in each year

OUTPUT FORMAT:

{
    "produce": [[produce_{k, t} for t in 1,...,T] for k in 1,...,K],
    "buildcapa": [[buildcapa_{k, t} for t in 1,...,T] for k in 1,...,K],
    "stockhold": [[stock_{k, t} for t in 1,...,T] for for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Indices}
\begin{itemize}
    \item $k$: Index for industry, $k = 1, 2, \ldots, K$
    \item $j$: Index for input industry, $j = 1, 2, \ldots, K$
    \item $t$: Index for time, $t = 0, 1, 2, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $inputone_{k,j}$: Input from industry $j$ required by industry $k$ for production
    \item $manpowerone_k$: Manpower required by industry $k$ for production
    \item $inputtwo_{k,j}$: Input from industry $j$ required by industry $k$ for building capacity
    \item $manpowertwo_k$: Manpower required by industry $k$ to build capacity
    \item $stock_k$: Initial stock of industry $k$ at year 0
    \item $capacity_k$: Initial capacity of industry $k$ at year 0
    \item $demand_k$: Demand for industry $k$ in every year except year 0
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $produce_{k,t}$: Amount produced by industry $k$ in year $t$
    \item $buildcapa_{k,t}$: Amount used to build productive capacity for industry $k$ in year $t$
    \item $stock_{k,t}$: Amount of stock of industry $k$ held in year $t$
\end{itemize}

\subsection*{Objective Function}
Maximize the total manpower requirement over five years:

\[
\text{Maximize} \quad \sum_{t=1}^{T} \sum_{k=1}^{K} (manpowerone_k \cdot produce_{k,t} + manpowertwo_k \cdot buildcapa_{k,t})
\]

\subsection*{Constraints}

\begin{align}
    & \text{Production Constraints:} \\
    & produce_{k,t} \leq stock_{k,t-1} + capacity_k \quad \forall k, t \\
    & stock_{k,t} = stock_{k,t-1} + produce_{k,t} - demand_k \quad \forall k, t \\
    & stock_{k,0} = stock_k \quad \forall k \\
    \\
    & \text{Input Constraints:} \\
    & \sum_{j=1}^{K} inputone_{k,j} \cdot produce_{j,t-1} + \sum_{j=1}^{K} inputtwo_{k,j} \cdot buildcapa_{j,t-1} \leq capacity_k \quad \forall k, t \\
    \\
    & \text{Manpower Constraints:} \\
    & manpowerone_k \cdot produce_{k,t} + manpowertwo_k \cdot buildcapa_{k,t} \leq \text{Available Manpower} \quad \forall k, t \\
    \\
    & \text{Non-negativity Constraints:} \\
    & produce_{k,t} \geq 0, \quad buildcapa_{k,t} \geq 0, \quad stock_{k,t} \geq 0 \quad \forall k, t
\end{align}

\subsection*{Output Variables}
\begin{itemize}
    \item Output $produce$ over the years
    \item Capacity building $buildcapa$ over the years
    \item Stock holding $stockhold$ over the years
\end{itemize}

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

\section*{Linear Programming Model}

\subsection*{Indices}
\begin{itemize}
    \item $k$: Index for industry, $k = 1, 2, \ldots, K$
    \item $j$: Index for input industry, $j = 1, 2, \ldots, K$
    \item $t$: Index for time, $t = 0, 1, 2, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $inputone_{k,j}$: Input from industry $j$ required by industry $k$ for production
    \item $manpowerone_k$: Manpower required by industry $k$ for production
    \item $inputtwo_{k,j}$: Input from industry $j$ required by industry $k$ for building capacity
    \item $manpowertwo_k$: Manpower required by industry $k$ to build capacity
    \item $stock_k$: Initial stock of industry $k$ at year 0
    \item $capacity_k$: Initial capacity of industry $k$ at year 0
    \item $demand_k$: Demand for industry $k$ in every year except year 0
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $produce_{k,t}$: Amount produced by industry $k$ in year $t$
    \item $buildcapa_{k,t}$: Amount used to build productive capacity for industry $k$ in year $t$
    \item $stock_{k,t}$: Amount of stock of industry $k$ held in year $t$
\end{itemize}

\subsection*{Objective Function}
Maximize the total manpower requirement over five years:

\[
\text{Maximize} \quad \sum_{t=1}^{T} \sum_{k=1}^{K} (manpowerone_k \cdot produce_{k,t} + manpowertwo_k \cdot buildcapa_{k,t})
\]

\subsection*{Constraints}

\begin{align}
    & \text{Production Constraints:} \\
    & produce_{k,t} \leq stock_{k,t-1} + capacity_k \quad \forall k, t \\
    & stock_{k,t} = stock_{k,t-1} + produce_{k,t} - demand_k \quad \forall k, t \\
    & stock_{k,0} = stock_k \quad \forall k \\
    \\
    & \text{Input Constraints:} \\
    & \sum_{j=1}^{K} inputone_{k,j} \cdot produce_{j,t-1} + \sum_{j=1}^{K} inputtwo_{k,j} \cdot buildcapa_{j,t-1} \leq capacity_k \quad \forall k, t \\
    \\
    & \text{Manpower Constraints:} \\
    & manpowerone_k \cdot produce_{k,t} + manpowertwo_k \cdot buildcapa_{k,t} \leq \text{Available Manpower} \quad \forall k, t \\
    \\
    & \text{Non-negativity Constraints:} \\
    & produce_{k,t} \geq 0, \quad buildcapa_{k,t} \geq 0, \quad stock_{k,t} \geq 0 \quad \forall k, t
\end{align}

\subsection*{Output Variables}
\begin{itemize}
    \item Output $produce$ over the years
    \item Capacity building $buildcapa$ over the years
    \item Stock holding $stockhold$ over the years
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pandas as pd
import pulp

#### Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  #### Number of industries
T = 5  #### Number of years

#### Create the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

#### Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (range(K), range(T+1)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                      for k in range(K) for t in range(1, T+1))

#### Constraints

#### Initial stocks
for k in range(K):
    problem += stock[k][0] == data['stock'][k]

#### Production Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k][t] <= stock[k][t-1] + data['capacity'][k]

#### Stock Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stock[k][t] == stock[k][t-1] + produce[k][t] - data['demand'][k]

#### Input Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + 
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K))) <= data['capacity'][k]

#### Manpower Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (data['manpowerone'][k] * produce[k][t] + 
                     data['manpowertwo'][k] * buildcapa[k][t] <= 
                     1)  #### Assuming Available Manpower is 1 for the sake of the model

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for k in range(K):
    for t in range(1, T+1):
        print(f'Produce[{k}][{t}]: {produce[k][t].varValue}, BuildCapa[{k}][{t}]: {buildcapa[k][t].varValue}, Stock[{k}][{t}]: {stock[k][t].varValue}')
```

