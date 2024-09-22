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
- There is a limited yearly manpower capacity of \var{manpower_limit}.


INPUT FORMAT:

{
    "inputone": [[inputone_{k, j} for j in 1,...,K] for k in 1,...,K],
    "manpowerone": [manpowerone_{k} for k in 1,...,K],
    "inputtwo": [[inputtwo_{k, j} for j in 1,...,K] for k in 1,...,K],
    "manpowertwo": [manpowertwo_{k} for k in 1,...,K],
    "stock": [stock_{k} for k in 1,...,K],
    "capacity": [capacity_{k} for k in 1,...,K],
    "manpower_limit": manpower_limit,
}


OBJECTIVE: Maximize total production in the last two years.

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

\section*{Linear Programming Model for Industry Production}

\subsection*{Indices}
\begin{itemize}
    \item $k$: Index for industries, where $k = 1, \ldots, K$
    \item $j$: Index for industries, where $j = 1, \ldots, K$
    \item $t$: Index for years, where $t = 1, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $inputone_{k,j}$: Input required from industry $j$ to produce in industry $k$
    \item $manpowerone_k$: Manpower required to produce in industry $k$
    \item $inputtwo_{k,j}$: Input required from industry $j$ to build capacity in industry $k$
    \item $manpowertwo_k$: Manpower required to build capacity in industry $k$
    \item $stock_k$: Initial stock of industry $k$ at year 0
    \item $capacity_k$: Capacity of industry $k$ at year 0
    \item $manpower_{limit}$: Maximum allowable manpower in a year
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $produce_{k,t}$: Amount of units produced by industry $k$ in year $t$
    \item $buildcapa_{k,t}$: Amount of units used to build productive capacity for industry $k$ in year $t$
    \item $stock_{k,t}$: Amount of stock of industry $k$ held in year $t$
\end{itemize}

\subsection*{Objective Function}
Maximize the total production in the last two years:
\[
\text{Maximize } Z = \sum_{k=1}^{K} (produce_{k,T} + produce_{k,T-1})
\]

\subsection*{Constraints}
\begin{align}
    & \text{Capacity constraints:} \\
    & produce_{k,t} \leq capacity_k + \sum_{j=1}^{K} buildcapa_{j,t-2} \quad \forall k, t \\
    & stock_{k,t} = stock_{k,t-1} + produce_{k,t-1} - \sum_{j=1}^{K} inputone_{j,k} \cdot produce_{j,t-1} \quad \forall k, t \\
    & stock_{k,t} \geq 0 \quad \forall k, t \\
    & \\
    & \text{Manpower constraints:} \\
    & \sum_{k=1}^{K} manpowerone_k \cdot produce_{k,t} + \sum_{k=1}^{K} manpowertwo_k \cdot buildcapa_{k,t} \leq manpower_{limit} \quad \forall t \\
    & \\
    & \text{Production constraint:} \\
    & produce_{k,t} \geq 0 \quad \forall k, t \\
    & buildcapa_{k,t} \geq 0 \quad \forall k, t \\
\end{align}

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

\section*{Linear Programming Model for Industry Production}

\subsection*{Indices}
\begin{itemize}
    \item $k$: Index for industries, where $k = 1, \ldots, K$
    \item $j$: Index for industries, where $j = 1, \ldots, K$
    \item $t$: Index for years, where $t = 1, \ldots, T$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $inputone_{k,j}$: Input required from industry $j$ to produce in industry $k$
    \item $manpowerone_k$: Manpower required to produce in industry $k$
    \item $inputtwo_{k,j}$: Input required from industry $j$ to build capacity in industry $k$
    \item $manpowertwo_k$: Manpower required to build capacity in industry $k$
    \item $stock_k$: Initial stock of industry $k$ at year 0
    \item $capacity_k$: Capacity of industry $k$ at year 0
    \item $manpower_{limit}$: Maximum allowable manpower in a year
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $produce_{k,t}$: Amount of units produced by industry $k$ in year $t$
    \item $buildcapa_{k,t}$: Amount of units used to build productive capacity for industry $k$ in year $t$
    \item $stock_{k,t}$: Amount of stock of industry $k$ held in year $t$
\end{itemize}

\subsection*{Objective Function}
Maximize the total production in the last two years:
\[
\text{Maximize } Z = \sum_{k=1}^{K} (produce_{k,T} + produce_{k,T-1})
\]

\subsection*{Constraints}
\begin{align}
    & \text{Capacity constraints:} \\
    & produce_{k,t} \leq capacity_k + \sum_{j=1}^{K} buildcapa_{j,t-2} \quad \forall k, t \\
    & stock_{k,t} = stock_{k,t-1} + produce_{k,t-1} - \sum_{j=1}^{K} inputone_{j,k} \cdot produce_{j,t-1} \quad \forall k, t \\
    & stock_{k,t} \geq 0 \quad \forall k, t \\
    & \\
    & \text{Manpower constraints:} \\
    & \sum_{k=1}^{K} manpowerone_k \cdot produce_{k,t} + \sum_{k=1}^{K} manpowertwo_k \cdot buildcapa_{k,t} \leq manpower_{limit} \quad \forall t \\
    & \\
    & \text{Production constraint:} \\
    & produce_{k,t} \geq 0 \quad \forall k, t \\
    & buildcapa_{k,t} \geq 0 \quad \forall k, t \\
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'manpower_limit': 470000000.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])  #### Number of industries
T = 5  #### Assuming a planning horizon of 5 years

#### Create a linear programming problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

#### Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(produce[k, T] + produce[k, T - 1] for k in range(K)), "Total_Production"

#### Capacity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[j, t - 2] for j in range(K) if t > 2), f"Capacity_Constraint_{k}_{t}"

#### Stock constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += stock[k, t] == data['stock'][k] + produce[k, t - 1], f"Stock_Constraint_{k}_{t}"
        else:
            problem += stock[k, t] == stock[k, t - 1] + produce[k, t - 1] - pulp.lpSum(data['inputone'][j][k] * produce[j, t - 1] for j in range(K)), f"Stock_Constraint_{k}_{t}"

#### Non-negativity constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += stock[k, t] >= 0, f"Non_Negative_Stock_{k}_{t}"

#### Manpower constraints
for t in range(1, T + 1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

#### Production constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += produce[k, t] >= 0, f"Non_Negative_Produce_{k}_{t}"
        problem += buildcapa[k, t] >= 0, f"Non_Negative_BuildCapa_{k}_{t}"

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

