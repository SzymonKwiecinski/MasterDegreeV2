# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP
PROBLEM INFO:

- An engineering factory makes several products on the machines, and the number of machine \var{m} the factory has is \var{num_{m}}.
- Each product \var{k} yields \var{profit_{k}} to profit (defined as £/unit selling price minus cost of raw materials).
- The unit production times (hours) product \var{k} requires on machine \var{m} is \var{time_{k, m}}
- In the present month (January) and several subsequent months, certain machines will be down for maintenance.
- Each machine \var{m} has to be down for \var{down_{m}} months for maintenance.
- There are marketing limitations on each product in each month. 
- The limitation of product \var{k} in month \var{i} is \var{limit_{k, i}}.
- It is possible to store up to 100 of each product at a time at a cost of \var{store_price} per unit per month. 
- There are no stocks at present, but it is desired to have a stock of \var{keep_quantity} of each type of product at the end of subsequent months.
- The factory works a six days a week with two shifts of \var{n_workhours} hours each day. 
- No sequencing problems need to be considered.
- We can assume that a month has 24 days for convenience.


INPUT FORMAT:

{
    "num_machines": [num_{m} for m in 1,...,M],
    "profit": [profit_{k} for k in 1,...K],
    "time": [[time_{k, m} for m in 1,...,M] for k in 1,...,K],
    "down": [down_{m} for m in 1,...,M]
    "limit": [[limit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "store_price": store_price,
    "keep_quantity": keep_quantity,
    "n_workhours": n_workhours
}

OBJECTIVE: What maintaining, selling, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO:

- \var{sell} represents the amount of selling quantity of each product in each month
- \var{manufacture} represents the amount of manufactured products in each month
- \var{storage} represents the storage of each product in each month
- \var{maintain} represents the number of machines in each type that are under maintenance in each month

OUTPUT FORMAT:

{
    "sell": [[sell_{k, i} for k in 1,...,K] for i in 1,...I],
    "manufacture": [[manufacture_{k, i} for k in 1,...,K] for i in 1,...I],
    "storage": [[storage_{k, i} for k in 1,...,K] for i in 1,...,I],
    "maintain": [[maintain_{m, k} for m in 1,...,M] for k in 1,...,K]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for MILP Problem}

\subsection*{Parameters}

\begin{align*}
& \text{Let } M \text{ be the number of machines} \\
& \text{Let } K \text{ be the number of products} \\
& \text{Let } I \text{ be the number of months} \\
& num_m = \{1, \ldots, M\} \\
& profit_k \text{ for } k \in \{1, \ldots, K\} \\
& time_{k, m} \text{ for } k \in \{1, \ldots, K\}, m \in \{1, \ldots, M\} \\
& down_m \text{ for } m \in \{1, \ldots, M\} \\
& limit_{k, i} \text{ for } k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
& store\_price \\
& keep\_quantity \\
& n\_workhours \\
& T = 24 \times 6 \text{ (total work hours per month)}
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
& sell_{k, i} \text{ = quantity of product } k \text{ sold in month } i \\
& manufacture_{k, i} \text{ = quantity of product } k \text{ manufactured in month } i \\
& storage_{k, i} \text{ = quantity of product } k \text{ stored at the end of month } i \\
& maintain_{m, k} \text{ = number of machines of type } m \text{ maintained for product } k
\end{align*}

\subsection*{Objective Function}

\begin{align*}
& \text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_k \cdot sell_{k, i} - \sum_{k=1}^{K} \sum_{i=1}^{I} store\_price \cdot storage_{k, i}
\end{align*}

\subsection*{Constraints}

\begin{align*}
& \sum_{k=1}^{K} sell_{k, i} \leq limit_{k, i} \quad \forall k, i \\
& \sum_{k=1}^{K} manufacture_{k, i} \cdot time_{k, m} \leq T \cdot (1 - \text{is\_down}_m) \quad \forall m, i \\
& \text{is\_down}_m = 
\begin{cases} 
1 & \text{if machine } m \text{ is down for maintenance} \\
0 & \text{otherwise}
\end{cases} \\
& storage_{k, i} = storage_{k, i-1} + manufacture_{k, i} - sell_{k, i} \quad \forall k, i \\
& storage_{k, I} \geq keep\_quantity \quad \forall k \\
& \sum_{m=1}^{M} maintain_{m, k} \leq down_m \quad \forall m, k \\
& sell_{k, i}, manufacture_{k, i}, storage_{k, i}, maintain_{m, k} \geq 0 \quad \forall k, i, m
\end{align*}

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

\section*{Mathematical Model for MILP Problem}

\subsection*{Parameters}

\begin{align*}
& \text{Let } M \text{ be the number of machines} \\
& \text{Let } K \text{ be the number of products} \\
& \text{Let } I \text{ be the number of months} \\
& num_m = \{1, \ldots, M\} \\
& profit_k \text{ for } k \in \{1, \ldots, K\} \\
& time_{k, m} \text{ for } k \in \{1, \ldots, K\}, m \in \{1, \ldots, M\} \\
& down_m \text{ for } m \in \{1, \ldots, M\} \\
& limit_{k, i} \text{ for } k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
& store\_price \\
& keep\_quantity \\
& n\_workhours \\
& T = 24 \times 6 \text{ (total work hours per month)}
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
& sell_{k, i} \text{ = quantity of product } k \text{ sold in month } i \\
& manufacture_{k, i} \text{ = quantity of product } k \text{ manufactured in month } i \\
& storage_{k, i} \text{ = quantity of product } k \text{ stored at the end of month } i \\
& maintain_{m, k} \text{ = number of machines of type } m \text{ maintained for product } k
\end{align*}

\subsection*{Objective Function}

\begin{align*}
& \text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_k \cdot sell_{k, i} - \sum_{k=1}^{K} \sum_{i=1}^{I} store\_price \cdot storage_{k, i}
\end{align*}

\subsection*{Constraints}

\begin{align*}
& \sum_{k=1}^{K} sell_{k, i} \leq limit_{k, i} \quad \forall k, i \\
& \sum_{k=1}^{K} manufacture_{k, i} \cdot time_{k, m} \leq T \cdot (1 - \text{is\_down}_m) \quad \forall m, i \\
& \text{is\_down}_m = 
\begin{cases} 
1 & \text{if machine } m \text{ is down for maintenance} \\
0 & \text{otherwise}
\end{cases} \\
& storage_{k, i} = storage_{k, i-1} + manufacture_{k, i} - sell_{k, i} \quad \forall k, i \\
& storage_{k, I} \geq keep\_quantity \quad \forall k \\
& \sum_{m=1}^{M} maintain_{m, k} \leq down_m \quad \forall m, k \\
& sell_{k, i}, manufacture_{k, i}, storage_{k, i}, maintain_{m, k} \geq 0 \quad \forall k, i, m
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import json
import pulp

#### Data in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
    ],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60],
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0,
}

#### Extracting data
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'])

profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
T = 24 * 6  #### Total work hours per month

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
sell = pulp.LpVariable.dicts("sell", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", [(m, k) for m in range(M) for k in range(K)], lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(profit[k] * sell[(k, i)] for k in range(K) for i in range(I)) - \
           pulp.lpSum(store_price * storage[(k, i)] for k in range(K) for i in range(I))

#### Constraints
for k in range(K):
    for i in range(I):
        problem += pulp.lpSum(sell[(k, i)] for k in range(K)) <= limit[i][k]

for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(manufacture[(k, i)] * time[k][m] for k in range(K)) <= T * (1 - down[m])

for k in range(K):
    for i in range(1, I):
        problem += storage[(k, i)] == storage[(k, i - 1)] + manufacture[(k, i)] - sell[(k, i)]

for k in range(K):
    problem += storage[(k, I - 1)] >= keep_quantity

for k in range(K):
    for m in range(M):
        problem += pulp.lpSum(maintain[(m, k)] for m in range(M)) <= down[m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

