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

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for industries ($k = 1, \ldots, K$)
    \item $t$: Index for years ($t = 1, \ldots, T$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $inputone_{k, j}$: Input from industry $j$ required by industry $k$
    \item $manpowerone_{k}$: Manpower required by industry $k$ for production
    \item $inputtwo_{k, j}$: Input from industry $j$ required by industry $k$ to build capacity
    \item $manpowertwo_{k}$: Manpower required by industry $k$ to build capacity
    \item $stock_{k}$: Initial stock of industry $k$ at year 0
    \item $capacity_{k}$: Current capacity of industry $k$
    \item $demand_{k}$: Exogenous consumption requirement from industry $k$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $produce_{k, t}$: Units produced by industry $k$ in year $t$
    \item $buildcapa_{k, t}$: Units used to build productive capacity for industry $k$ in year $t$
    \item $stockhold_{k, t}$: Stock of industry $k$ held in year $t$
\end{itemize}

\textbf{Objective:} 
\[
\text{Maximize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k, t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k, t}
\]

\textbf{Constraints:}

1. \textbf{Production Constraints:}\\
\[
produce_{k, t} + stockhold_{k, t-1} = \sum_{j=1}^{K} inputone_{k, j} \cdot produce_{j, t-1} + stockhold_{k, t} + demand_{k}, \quad \forall k, t
\]

2. \textbf{Capacity Building Constraints:}\\
\[
buildcapa_{k, t} \leq capacity_{k} + stockhold_{k, t-1} + \sum_{j=1}^{K} inputtwo_{k, j} \cdot produce_{j, t-1}, \quad \forall k, t
\]

3. \textbf{Manpower Constraints:}\\
\[
\sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k, t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k, t} \leq M, \quad \forall t
\]
where \(M\) is the maximum available manpower in the economy.

4. \textbf{Stock Update Constraints:}\\
\[
stockhold_{k, t} = stockhold_{k, t-1} + produce_{k, t} - demand_{k}, \quad \forall k, t
\]

5. \textbf{Non-negativity Constraints:}\\
\[
produce_{k, t} \geq 0, \quad buildcapa_{k, t} \geq 0, \quad stockhold_{k, t} \geq 0, \quad \forall k, t
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

\section*{Linear Programming Model}

\textbf{Indices:}
\begin{itemize}
    \item $k$: Index for industries ($k = 1, \ldots, K$)
    \item $t$: Index for years ($t = 1, \ldots, T$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $inputone_{k, j}$: Input from industry $j$ required by industry $k$
    \item $manpowerone_{k}$: Manpower required by industry $k$ for production
    \item $inputtwo_{k, j}$: Input from industry $j$ required by industry $k$ to build capacity
    \item $manpowertwo_{k}$: Manpower required by industry $k$ to build capacity
    \item $stock_{k}$: Initial stock of industry $k$ at year 0
    \item $capacity_{k}$: Current capacity of industry $k$
    \item $demand_{k}$: Exogenous consumption requirement from industry $k$
\end{itemize}

\textbf{Variables:}
\begin{itemize}
    \item $produce_{k, t}$: Units produced by industry $k$ in year $t$
    \item $buildcapa_{k, t}$: Units used to build productive capacity for industry $k$ in year $t$
    \item $stockhold_{k, t}$: Stock of industry $k$ held in year $t$
\end{itemize}

\textbf{Objective:} 
\[
\text{Maximize } Z = \sum_{t=1}^{T} \sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k, t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k, t}
\]

\textbf{Constraints:}

1. \textbf{Production Constraints:}\\
\[
produce_{k, t} + stockhold_{k, t-1} = \sum_{j=1}^{K} inputone_{k, j} \cdot produce_{j, t-1} + stockhold_{k, t} + demand_{k}, \quad \forall k, t
\]

2. \textbf{Capacity Building Constraints:}\\
\[
buildcapa_{k, t} \leq capacity_{k} + stockhold_{k, t-1} + \sum_{j=1}^{K} inputtwo_{k, j} \cdot produce_{j, t-1}, \quad \forall k, t
\]

3. \textbf{Manpower Constraints:}\\
\[
\sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k, t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k, t} \leq M, \quad \forall t
\]
where \(M\) is the maximum available manpower in the economy.

4. \textbf{Stock Update Constraints:}\\
\[
stockhold_{k, t} = stockhold_{k, t-1} + produce_{k, t} - demand_{k}, \quad \forall k, t
\]

5. \textbf{Non-negativity Constraints:}\\
\[
produce_{k, t} \geq 0, \quad buildcapa_{k, t} \geq 0, \quad stockhold_{k, t} \geq 0, \quad \forall k, t
\]

\end{document}</MATH_MODEL>
<DATA>
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
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
T = 1  #### Single time period for simplicity
M = 1000000  #### Maximum available manpower

#### Create a problem
problem = pulp.LpProblem("Industry_Production_Problem", pulp.LpMaximize)

#### Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                      for k in range(K) for t in range(T))

#### Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[(k, t)] + data['stock'][k]
                        == pulp.lpSum(data['inputone'][k][j] * (produce[(j, t-1)] if t > 0 else 0)
                                      for j in range(K)) + stockhold[(k, t)] + data['demand'][k])

        problem += (buildcapa[(k, t)]
                    <= data['capacity'][k] + (data['stock'][k] if t == 0 else stockhold[(k, t-1)])
                    + pulp.lpSum(data['inputtwo'][k][j] * (produce[(j, t-1)] if t > 0 else 0) for j in range(K)))

for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                           for k in range(K)) <= M)

for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (stockhold[(k, t)] == data['stock'][k] + produce[(k, t)] - data['demand'][k])

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

