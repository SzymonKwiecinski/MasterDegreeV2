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

\section*{Mathematical Model for Manufacturing Problem}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( m \) : Index for machines, \( m = 1, \ldots, M \)
    \item \( k \) : Index for products, \( k = 1, \ldots, K \)
    \item \( i \) : Index for months, \( i = 1, \ldots, I \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{num}_{m} \): Number of machines 
    \item \( \text{profit}_{k} \): Profit from product \( k \) (£/unit)
    \item \( \text{time}_{k, m} \): Production time (hours) for product \( k \) on machine \( m \)
    \item \( \text{down}_{m} \): Months machine \( m \) is down for maintenance
    \item \( \text{limit}_{k, i} \): Marketing limitation for product \( k \) in month \( i \)
    \item \( \text{store\_price} \): Storage cost per unit per month
    \item \( \text{keep\_quantity} \): Desired stock of product at the end of each month
    \item \( \text{n\_workhours} \): Total work hours available in a month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{sell}_{k, i} \): Amount of product \( k \) sold in month \( i \)
    \item \( \text{manufacture}_{k, i} \): Amount of product \( k \) manufactured in month \( i \)
    \item \( \text{storage}_{k, i} \): Amount of product \( k \) stored at the end of month \( i \)
    \item \( \text{maintain}_{m, i} \): Amount of machine \( m \) in maintenance during month \( i \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{i=1}^{I} \left( \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{sell}_{k, i} - \sum_{k=1}^{K} \text{store\_price} \cdot \text{storage}_{k, i} \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Production Time Constraint:} & \quad \sum_{k=1}^{K} \text{time}_{k, m} \cdot \text{manufacture}_{k, i} \leq \text{n\_workhours} \cdot (1 - \text{down}_{m}) \quad \forall m, i\\
\text{Marketing Limitations:} & \quad \text{sell}_{k, i} \leq \text{limit}_{k, i} \quad \forall k, i\\
\text{Inventory Balance:} & \quad \text{storage}_{k, i} = \text{storage}_{k, i-1} + \text{manufacture}_{k, i} - \text{sell}_{k, i} \quad \forall k, i\\
& \quad \text{storage}_{k, 0} = 0 \quad \forall k \\
\text{Desired Ending Inventory:} & \quad \text{storage}_{k, I} \geq \text{keep\_quantity} \quad \forall k\\
\text{Non-negativity Constraints:} & \quad \text{sell}_{k, i}, \text{manufacture}_{k, i}, \text{storage}_{k, i} \geq 0 \quad \forall k, i\\
& \quad \text{maintain}_{m, i} \in \{0, 1\} \quad \forall m, i
\end{align*}

\subsection*{Output}
\begin{itemize}
    \item \text{sell}: \( \text{sell}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{manufacture}: \( \text{manufacture}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{storage}: \( \text{storage}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{maintain}: \( \text{maintain}_{m, i} \) for \( m \in \{1,\ldots,M\}, k \in \{1,\ldots,K\} \)
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

\section*{Mathematical Model for Manufacturing Problem}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( m \) : Index for machines, \( m = 1, \ldots, M \)
    \item \( k \) : Index for products, \( k = 1, \ldots, K \)
    \item \( i \) : Index for months, \( i = 1, \ldots, I \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{num}_{m} \): Number of machines 
    \item \( \text{profit}_{k} \): Profit from product \( k \) (£/unit)
    \item \( \text{time}_{k, m} \): Production time (hours) for product \( k \) on machine \( m \)
    \item \( \text{down}_{m} \): Months machine \( m \) is down for maintenance
    \item \( \text{limit}_{k, i} \): Marketing limitation for product \( k \) in month \( i \)
    \item \( \text{store\_price} \): Storage cost per unit per month
    \item \( \text{keep\_quantity} \): Desired stock of product at the end of each month
    \item \( \text{n\_workhours} \): Total work hours available in a month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{sell}_{k, i} \): Amount of product \( k \) sold in month \( i \)
    \item \( \text{manufacture}_{k, i} \): Amount of product \( k \) manufactured in month \( i \)
    \item \( \text{storage}_{k, i} \): Amount of product \( k \) stored at the end of month \( i \)
    \item \( \text{maintain}_{m, i} \): Amount of machine \( m \) in maintenance during month \( i \)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize} \quad Z = \sum_{i=1}^{I} \left( \sum_{k=1}^{K} \text{profit}_{k} \cdot \text{sell}_{k, i} - \sum_{k=1}^{K} \text{store\_price} \cdot \text{storage}_{k, i} \right)
\]

\subsection*{Constraints}
\begin{align*}
\text{Production Time Constraint:} & \quad \sum_{k=1}^{K} \text{time}_{k, m} \cdot \text{manufacture}_{k, i} \leq \text{n\_workhours} \cdot (1 - \text{down}_{m}) \quad \forall m, i\\
\text{Marketing Limitations:} & \quad \text{sell}_{k, i} \leq \text{limit}_{k, i} \quad \forall k, i\\
\text{Inventory Balance:} & \quad \text{storage}_{k, i} = \text{storage}_{k, i-1} + \text{manufacture}_{k, i} - \text{sell}_{k, i} \quad \forall k, i\\
& \quad \text{storage}_{k, 0} = 0 \quad \forall k \\
\text{Desired Ending Inventory:} & \quad \text{storage}_{k, I} \geq \text{keep\_quantity} \quad \forall k\\
\text{Non-negativity Constraints:} & \quad \text{sell}_{k, i}, \text{manufacture}_{k, i}, \text{storage}_{k, i} \geq 0 \quad \forall k, i\\
& \quad \text{maintain}_{m, i} \in \{0, 1\} \quad \forall m, i
\end{align*}

\subsection*{Output}
\begin{itemize}
    \item \text{sell}: \( \text{sell}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{manufacture}: \( \text{manufacture}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{storage}: \( \text{storage}_{k, i} \) for \( k \in \{1,\ldots,K\}, i \in \{1,\ldots,I\} \)
    \item \text{maintain}: \( \text{maintain}_{m, i} \) for \( m \in \{1,\ldots,M\}, k \in \{1,\ldots,K\} \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

#### Extracting parameters from data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Constants
M = len(num_machines)  #### number of machines
K = len(profit)        #### number of products
I = len(limit[0])      #### number of months

#### Model
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[m][i], f"Marketing_Limit_k{k}_i{i}"

for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Inventory_Balance_k{k}_i{i}"

for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_k{k}"

for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"Desired_Ending_Inventory_k{k}"

#### Non-negativity and binary constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] >= 0
        problem += manufacture[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(M):
    for i in range(I):
        problem += maintain[m][i] in [0, 1]

#### Solve the problem
problem.solve()

#### Output the results
for k in range(K):
    for i in range(I):
        print(f'sell_{k}_{i}: {sell[k][i].varValue}, manufacture_{k}_{i}: {manufacture[k][i].varValue}, storage_{k}_{i}: {storage[k][i].varValue}')

for m in range(M):
    for i in range(I):
        print(f'maintain_{m}_{i}: {maintain[m][i].varValue}')

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

#### Data input
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

#### Extracting parameters from data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Constants
M = len(num_machines)  #### number of machines
K = len(profit)        #### number of products
I = len(limit[0])      #### number of months

#### Model
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[m][i], f"Marketing_Limit_k{k}_i{i}"

for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Inventory_Balance_k{k}_i{i}"

for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_k{k}"

for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"Desired_Ending_Inventory_k{k}"

#### Non-negativity and binary constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] >= 0
        problem += manufacture[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(M):
    for i in range(I):
        problem += maintain[m][i] in [0, 1]

#### Solve the problem
problem.solve()

#### Output the results
for k in range(K):
    for i in range(I):
        print(f'sell_{k}_{i}: {sell[k][i].varValue}, manufacture_{k}_{i}: {manufacture[k][i].varValue}, storage_{k}_{i}: {storage[k][i].varValue}')

for m in range(M):
    for i in range(I):
        print(f'maintain_{m}_{i}: {maintain[m][i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/6/21/python_code0.py", line 37, in <module>
    problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/6/21/python_code0.py", line 37, in <genexpr>
    problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"
                          ~~~~^^^
IndexError: list index out of range
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

#### Extracting parameters from data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Constants
M = len(num_machines)  #### number of machines
K = len(profit)        #### number of products
I = len(limit[0])      #### number of months

#### Model
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] for k in range(K) for i in range(I)) - pulp.lpSum(store_price * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) if m < len(time[k])) <= n_workhours * (1 - down[m]), f"Production_Time_Constraint_m{m}_i{i}"

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i], f"Marketing_Limit_k{k}_i{i}"

for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Inventory_Balance_k{k}_i{i}"

for k in range(K):
    problem += storage[k][0] == 0, f"Initial_Storage_k{k}"

for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"Desired_Ending_Inventory_k{k}"

#### Non-negativity and binary constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] >= 0
        problem += manufacture[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(M):
    for i in range(I):
        problem += maintain[m][i] in [0, 1]

#### Solve the problem
problem.solve()

#### Output the results
for k in range(K):
    for i in range(I):
        print(f'sell_{k}_{i}: {sell[k][i].varValue}, manufacture_{k}_{i}: {manufacture[k][i].varValue}, storage_{k}_{i}: {storage[k][i].varValue}')

for m in range(M):
    for i in range(I):
        print(f'maintain_{m}_{i}: {maintain[m][i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

