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

\section*{Linear Programming Model for Industry Production}

\subsection*{Parameters}

Let:
\begin{itemize}
    \item \( K \) = Number of industries 
    \item \( T \) = Planning horizon (5 years)
    \item \( \text{inputone}_{k,j} \) = Input from industry \( j \) required by industry \( k \)
    \item \( \text{manpowerone}_{k} \) = Manpower required by industry \( k \)
    \item \( \text{inputtwo}_{k,j} \) = Input from industry \( j \) needed to build capacity for industry \( k \)
    \item \( \text{manpowertwo}_{k} \) = Manpower required to build capacity for industry \( k \)
    \item \( \text{stock}_{k} \) = Initial stock of industry \( k \)
    \item \( \text{capacity}_{k} \) = Initial capacity of industry \( k \)
    \item \( \text{demand}_{k} \) = Exogenous demand from industry \( k \)
\end{itemize}

\subsection*{Variables}

Define:
\begin{itemize}
    \item \( \text{produce}_{k,t} \) = Amount produced by industry \( k \) in year \( t \)
    \item \( \text{buildcapa}_{k,t} \) = Amount used to build productive capacity for industry \( k \) in year \( t \)
    \item \( \text{stockhold}_{k,t} \) = Amount of stock held by industry \( k \) in year \( t \)
\end{itemize}

\subsection*{Objective Function}

Maximize the total manpower requirement over five years:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \sum_{t=1}^{T} \left( \text{manpowerone}_{k} \cdot \text{produce}_{k,t} + \text{manpowertwo}_{k} \cdot \text{buildcapa}_{k,t} \right)
\]

\subsection*{Constraints}

1. **Demand constraint for each industry** (for \( t = 1, \ldots, T \)):
   \[
   \text{produce}_{k,t} + \text{stockhold}_{k,t-1} - \text{stockhold}_{k,t} \geq \text{demand}_{k}, \quad \forall k, t
   \]

2. **Production capacity constraint**:
   \[
   \text{produce}_{k,t} \leq \text{capacity}_{k} + \text{capacity\_increase}_{k,t-2}, \quad \forall k, t \text{ (for } t \geq 2\text{)}
   \]
   
   where \( \text{capacity\_increase}_{k,t-2} = \sum_{j=1}^{K} \text{buildcapa}_{j,t-2} \cdot \text{inputtwo}_{j,k} \)

3. **Stock balance**:
   \[
   \text{stockhold}_{k,t} = \text{stockhold}_{k,t-1} + \text{produce}_{k,t} - \text{demand}_{k}, \quad \forall k, t
   \]

4. **Initial conditions**:
   \[
   \text{stockhold}_{k,0} = \text{stock}_{k}, \quad \text{capacity}_{k,0} = \text{capacity}_{k}, \quad \forall k
   \]

5. **Non-negativity**:
   \[
   \text{produce}_{k,t} \geq 0, \quad \text{buildcapa}_{k,t} \geq 0, \quad \text{stockhold}_{k,t} \geq 0, \quad \forall k, t
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

\section*{Linear Programming Model for Industry Production}

\subsection*{Parameters}

Let:
\begin{itemize}
    \item \( K \) = Number of industries 
    \item \( T \) = Planning horizon (5 years)
    \item \( \text{inputone}_{k,j} \) = Input from industry \( j \) required by industry \( k \)
    \item \( \text{manpowerone}_{k} \) = Manpower required by industry \( k \)
    \item \( \text{inputtwo}_{k,j} \) = Input from industry \( j \) needed to build capacity for industry \( k \)
    \item \( \text{manpowertwo}_{k} \) = Manpower required to build capacity for industry \( k \)
    \item \( \text{stock}_{k} \) = Initial stock of industry \( k \)
    \item \( \text{capacity}_{k} \) = Initial capacity of industry \( k \)
    \item \( \text{demand}_{k} \) = Exogenous demand from industry \( k \)
\end{itemize}

\subsection*{Variables}

Define:
\begin{itemize}
    \item \( \text{produce}_{k,t} \) = Amount produced by industry \( k \) in year \( t \)
    \item \( \text{buildcapa}_{k,t} \) = Amount used to build productive capacity for industry \( k \) in year \( t \)
    \item \( \text{stockhold}_{k,t} \) = Amount of stock held by industry \( k \) in year \( t \)
\end{itemize}

\subsection*{Objective Function}

Maximize the total manpower requirement over five years:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \sum_{t=1}^{T} \left( \text{manpowerone}_{k} \cdot \text{produce}_{k,t} + \text{manpowertwo}_{k} \cdot \text{buildcapa}_{k,t} \right)
\]

\subsection*{Constraints}

1. **Demand constraint for each industry** (for \( t = 1, \ldots, T \)):
   \[
   \text{produce}_{k,t} + \text{stockhold}_{k,t-1} - \text{stockhold}_{k,t} \geq \text{demand}_{k}, \quad \forall k, t
   \]

2. **Production capacity constraint**:
   \[
   \text{produce}_{k,t} \leq \text{capacity}_{k} + \text{capacity\_increase}_{k,t-2}, \quad \forall k, t \text{ (for } t \geq 2\text{)}
   \]
   
   where \( \text{capacity\_increase}_{k,t-2} = \sum_{j=1}^{K} \text{buildcapa}_{j,t-2} \cdot \text{inputtwo}_{j,k} \)

3. **Stock balance**:
   \[
   \text{stockhold}_{k,t} = \text{stockhold}_{k,t-1} + \text{produce}_{k,t} - \text{demand}_{k}, \quad \forall k, t
   \]

4. **Initial conditions**:
   \[
   \text{stockhold}_{k,0} = \text{stock}_{k}, \quad \text{capacity}_{k,0} = \text{capacity}_{k}, \quad \forall k
   \]

5. **Non-negativity**:
   \[
   \text{produce}_{k,t} \geq 0, \quad \text{buildcapa}_{k,t} \geq 0, \quad \text{stockhold}_{k,t} \geq 0, \quad \forall k, t
   \]

\end{document}</MATH_MODEL>
<DATA>
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data in JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

#### Parameters
K = len(data['manpowerone'])  #### Number of industries
T = 5  #### Planning horizon (5 years)
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

#### Create the problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

#### Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K) for t in range(T)), "Total_Manpower"

#### Constraints
#### Initial stock and capacity
for k in range(K):
    problem += (stockhold[k][0] == stock[k]), f"Initial_Stock_{k}"
    problem += (stockhold[k][0] == stock[k]), f"Initial_Capacity_{k}"

#### Demand Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[k][t] + stockhold[k][t] - demand[k] >= 0), f"Demand_Constraint_{k}_{t}"
        else:
            problem += (produce[k][t] + stockhold[k][t-1] - stockhold[k][t] >= demand[k]), f"Demand_Constraint_{k}_{t}"

#### Production capacity constraint
for k in range(K):
    for t in range(2, T):
        capacity_increase = pulp.lpSum(buildcapa[j][t-2] * inputtwo[j][k] for j in range(K))
        problem += (produce[k][t] <= capacity[k] + capacity_increase), f"Production_Capacity_{k}_{t}"

#### Stock balance
for k in range(K):
    for t in range(1, T):
        problem += (stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - demand[k]), f"Stock_Balance_{k}_{t}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

