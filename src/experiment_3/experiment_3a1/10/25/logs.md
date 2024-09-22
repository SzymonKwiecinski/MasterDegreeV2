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

\section*{Linear Programming Model}

Let:
\begin{itemize}
    \item \( K \) be the number of industries.
    \item \( T \) be the time horizon (number of years).
    \item \( produce_{k,t} \) be the amount produced by industry \( k \) in year \( t \).
    \item \( buildcapa_{k,t} \) be the amount used to build capacity by industry \( k \) in year \( t \).
    \item \( stock_{k,t} \) be the stock held by industry \( k \) at the end of year \( t \).
\end{itemize}

\subsection*{Objective Function}

Maximize total production in the last two years:
\[
\text{Maximize } Z = \sum_{k=1}^{K} (produce_{k,T-1} + produce_{k,T})
\]

\subsection*{Constraints}

1. **Production Constraints for Each Industry**:
   For each industry \( k \) in year \( t \):
   \[
   produce_{k,t} \leq capacity_{k} + stock_{k,t-1}
   \]

2. **Input Requirements for Production**:
   For industry \( k \) in year \( t \):
   \[
   \sum_{j=1}^{K} inputone_{k,j} \cdot produce_{j,t-1} + manpowerone_{k} \cdot produce_{k,t} \leq stock_{k,t-1} + capacity_{k}
   \]

3. **Manpower Constraints**:
   The total manpower used in any year cannot exceed the available manpower limit:
   \[
   \sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k,t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k,t} \leq manpower\_limit
   \]

4. **Capacity Building**:
   To build capacity in year \( t \):
   \[
   buildcapa_{k,t} \leq stock_{k,t-1}
   \]

5. **Stock Dynamics**:
   The stock for each industry at the end of year \( t \) is given by:
   \[
   stock_{k,t} = stock_{k,t-1} + produce_{k,t} - \sum_{j=1}^{K} inputone_{j,k} \cdot produce_{j,t-1} - buildcapa_{k,t}
   \]

6. **Initial Conditions**:
   At year \( 0 \):
   \[
   stock_{k,0} = stock_{k}
   \]
   \[
   capacity_{k,0} = capacity_{k}
   \]

7. **Non-negativity Constraints**:
   \[
   produce_{k,t} \geq 0, \quad buildcapa_{k,t} \geq 0, \quad stock_{k,t} \geq 0
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

Let:
\begin{itemize}
    \item \( K \) be the number of industries.
    \item \( T \) be the time horizon (number of years).
    \item \( produce_{k,t} \) be the amount produced by industry \( k \) in year \( t \).
    \item \( buildcapa_{k,t} \) be the amount used to build capacity by industry \( k \) in year \( t \).
    \item \( stock_{k,t} \) be the stock held by industry \( k \) at the end of year \( t \).
\end{itemize}

\subsection*{Objective Function}

Maximize total production in the last two years:
\[
\text{Maximize } Z = \sum_{k=1}^{K} (produce_{k,T-1} + produce_{k,T})
\]

\subsection*{Constraints}

1. **Production Constraints for Each Industry**:
   For each industry \( k \) in year \( t \):
   \[
   produce_{k,t} \leq capacity_{k} + stock_{k,t-1}
   \]

2. **Input Requirements for Production**:
   For industry \( k \) in year \( t \):
   \[
   \sum_{j=1}^{K} inputone_{k,j} \cdot produce_{j,t-1} + manpowerone_{k} \cdot produce_{k,t} \leq stock_{k,t-1} + capacity_{k}
   \]

3. **Manpower Constraints**:
   The total manpower used in any year cannot exceed the available manpower limit:
   \[
   \sum_{k=1}^{K} manpowerone_{k} \cdot produce_{k,t} + \sum_{k=1}^{K} manpowertwo_{k} \cdot buildcapa_{k,t} \leq manpower\_limit
   \]

4. **Capacity Building**:
   To build capacity in year \( t \):
   \[
   buildcapa_{k,t} \leq stock_{k,t-1}
   \]

5. **Stock Dynamics**:
   The stock for each industry at the end of year \( t \) is given by:
   \[
   stock_{k,t} = stock_{k,t-1} + produce_{k,t} - \sum_{j=1}^{K} inputone_{j,k} \cdot produce_{j,t-1} - buildcapa_{k,t}
   \]

6. **Initial Conditions**:
   At year \( 0 \):
   \[
   stock_{k,0} = stock_{k}
   \]
   \[
   capacity_{k,0} = capacity_{k}
   \]

7. **Non-negativity Constraints**:
   \[
   produce_{k,t} \geq 0, \quad buildcapa_{k,t} \geq 0, \quad stock_{k,t} \geq 0
   \]

\end{document}</MATH_MODEL>
<DATA>
{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'manpower_limit': 470000000.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    "manpowerone": [0.6, 0.3, 0.2], 
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    "manpowertwo": [0.4, 0.2, 0.1], 
    "stock": [150, 80, 100], 
    "capacity": [300, 350, 280], 
    "manpower_limit": 470000000.0
}'''
data = json.loads(data)

#### Model Parameters
K = len(data['manpowerone'])  #### Number of industries
T = 2  #### Time horizon (last two years are T-1 and T)

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

#### Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (k for k in range(K)), lowBound=0)

#### Objective Function
problem += pulp.lpSum([produce[k, T-1] + produce[k, T] for k in range(K)])

#### Constraints
#### Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stock[k] if t == 0 else stock[k])

#### Input Requirements for Production
for k in range(K):
    for t in range(T):
        inputs = pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K))
        problem += inputs + data['manpowerone'][k] * produce[k, t] <= stock[k] + data['capacity'][k]

#### Manpower Constraints
for t in range(T):
    manpower_used = pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + \
                    pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
    problem += manpower_used <= data['manpower_limit']

#### Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k, t] <= stock[k]

#### Stock Dynamics
for k in range(K):
    for t in range(1, T):
        problem += stock[k] == stock[k] + produce[k, t] - \
                   pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)) - buildcapa[k, t]

#### Initial Conditions at year 0
for k in range(K):
    stock[k] = data['stock'][k]
    capacity = data['capacity'][k]

#### Solve the problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

