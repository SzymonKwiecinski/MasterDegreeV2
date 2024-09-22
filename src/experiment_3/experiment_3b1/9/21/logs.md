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

\section*{Mathematical Model for Manufacturing Optimization}

\textbf{Indices:}
\begin{itemize}
    \item $k$: index for products ($k = 1, \ldots, K$)
    \item $m$: index for machines ($m = 1, \ldots, M$)
    \item $i$: index for months ($i = 1, \ldots, I$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $num_{m}$: number of machines
    \item $profit_{k}$: profit per unit of product $k$
    \item $time_{k, m}$: production time required for product $k$ on machine $m$
    \item $down_{m}$: downtime for machine $m$ 
    \item $limit_{k, i}$: sales limit for product $k$ in month $i$
    \item $store\_price$: storage cost per unit per month
    \item $keep\_quantity$: desired ending inventory for each product
    \item $n\_workhours$: total working hours available per month
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $sell_{k, i}$: quantity sold of product $k$ in month $i$
    \item $manufacture_{k, i}$: quantity manufactured of product $k$ in month $i$
    \item $storage_{k, i}$: quantity stored of product $k$ at the end of month $i$
    \item $maintain_{m, i}$: binary variable indicating if machine $m$ is under maintenance in month $i$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize: } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_{k} \cdot sell_{k, i} - \sum_{i=1}^{I} \sum_{k=1}^{K} store\_price \cdot storage_{k, i}
\]

\textbf{Constraints:}

1. \textbf{Production Time Constraint:}
\[
\sum_{k=1}^{K} time_{k, m} \cdot manufacture_{k, i} \leq (n\_workhours \cdot (24 - \sum_{j=1}^{i} down_{m})) \cdot (1 - maintain_{m, i}), \quad \forall m, i
\]

2. \textbf{Sales Limit Constraint:}
\[
sell_{k, i} \leq limit_{k, i}, \quad \forall k, i
\]

3. \textbf{Storage Constraints:}
\[
storage_{k, i} = storage_{k, i-1} + manufacture_{k, i} - sell_{k, i}, \quad \forall k, i > 1
\]
\[
storage_{k, 1} = 0, \quad \forall k
\]
\[
storage_{k, i} \leq 100, \quad \forall k, i
\]

4. \textbf{Ending Inventory Constraint:}
\[
storage_{k, I} \geq keep\_quantity, \quad \forall k
\]

5. \textbf{Non-negativity and Binary Constraints:}
\[
sell_{k, i} \geq 0, \quad manufacture_{k, i} \geq 0, \quad storage_{k, i} \geq 0, \quad \forall k, i
\]
\[
maintain_{m, i} \in \{0, 1\}, \quad \forall m, i
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

\section*{Mathematical Model for Manufacturing Optimization}

\textbf{Indices:}
\begin{itemize}
    \item $k$: index for products ($k = 1, \ldots, K$)
    \item $m$: index for machines ($m = 1, \ldots, M$)
    \item $i$: index for months ($i = 1, \ldots, I$)
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $num_{m}$: number of machines
    \item $profit_{k}$: profit per unit of product $k$
    \item $time_{k, m}$: production time required for product $k$ on machine $m$
    \item $down_{m}$: downtime for machine $m$ 
    \item $limit_{k, i}$: sales limit for product $k$ in month $i$
    \item $store\_price$: storage cost per unit per month
    \item $keep\_quantity$: desired ending inventory for each product
    \item $n\_workhours$: total working hours available per month
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $sell_{k, i}$: quantity sold of product $k$ in month $i$
    \item $manufacture_{k, i}$: quantity manufactured of product $k$ in month $i$
    \item $storage_{k, i}$: quantity stored of product $k$ at the end of month $i$
    \item $maintain_{m, i}$: binary variable indicating if machine $m$ is under maintenance in month $i$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize: } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_{k} \cdot sell_{k, i} - \sum_{i=1}^{I} \sum_{k=1}^{K} store\_price \cdot storage_{k, i}
\]

\textbf{Constraints:}

1. \textbf{Production Time Constraint:}
\[
\sum_{k=1}^{K} time_{k, m} \cdot manufacture_{k, i} \leq (n\_workhours \cdot (24 - \sum_{j=1}^{i} down_{m})) \cdot (1 - maintain_{m, i}), \quad \forall m, i
\]

2. \textbf{Sales Limit Constraint:}
\[
sell_{k, i} \leq limit_{k, i}, \quad \forall k, i
\]

3. \textbf{Storage Constraints:}
\[
storage_{k, i} = storage_{k, i-1} + manufacture_{k, i} - sell_{k, i}, \quad \forall k, i > 1
\]
\[
storage_{k, 1} = 0, \quad \forall k
\]
\[
storage_{k, i} \leq 100, \quad \forall k, i
\]

4. \textbf{Ending Inventory Constraint:}
\[
storage_{k, I} \geq keep\_quantity, \quad \forall k
\]

5. \textbf{Non-negativity and Binary Constraints:}
\[
sell_{k, i} \geq 0, \quad manufacture_{k, i} \geq 0, \quad storage_{k, i} \geq 0, \quad \forall k, i
\]
\[
maintain_{m, i} \in \{0, 1\}, \quad \forall m, i
\]

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

K = len(data['profit'])
M = len(data['num_machines'])
I = len(data['limit'][0])

#### Create a Linear Programming problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
#### Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(K)) <= \
                   (data['n_workhours'] * (24 - sum(data['down'][0][j] for j in range(i + 1)))) * \
                   (1 - maintain[m][i])

#### Sales Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

#### Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    problem += storage[k][0] == 0
    problem += storage[k][i] <= 100

#### Ending Inventory Constraint
for k in range(K):
    problem += storage[k][I-1] >= data['keep_quantity']

#### Solve the problem
problem.solve()

#### Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp
import json

data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

K = len(data['profit'])
M = len(data['num_machines'])
I = len(data['limit'][0])

#### Create a Linear Programming problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
#### Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(K)) <= \
                   (data['n_workhours'] * (24 - sum(data['down'][0][j] for j in range(i + 1)))) * \
                   (1 - maintain[m][i])

#### Sales Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

#### Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    problem += storage[k][0] == 0
    problem += storage[k][i] <= 100

#### Ending Inventory Constraint
for k in range(K):
    problem += storage[k][I-1] >= data['keep_quantity']

#### Solve the problem
problem.solve()

#### Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/9/21/python_code0.py", line 51, in <module>
    problem += pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(K)) <= \
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/9/21/python_code0.py", line 51, in <genexpr>
    problem += pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(K)) <= \
                          ~~~~^^^^^^^^^^^^^^
KeyError: 'time[k][m]'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'down': [[0, 1, 1, 1, 1]],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

K = len(data['profit'])
M = len(data['num_machines'])
I = len(data['limit'][0])

#### Create a Linear Programming problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I)) - \
           pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
#### Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K)) <= \
                   (data['n_workhours'] * (24 - sum(data['down'][0][j] for j in range(i + 1)))) * \
                   (1 - maintain[m][i])

#### Sales Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

#### Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    problem += storage[k][0] == 0
    problem += storage[k][i] <= 100

#### Ending Inventory Constraint
for k in range(K):
    problem += storage[k][I-1] >= data['keep_quantity']

#### Solve the problem
problem.solve()

#### Output the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

