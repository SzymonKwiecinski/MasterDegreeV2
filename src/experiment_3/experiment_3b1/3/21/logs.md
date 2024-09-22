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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item $M$: Set of machines, $m \in M$
    \item $K$: Set of products, $k \in K$
    \item $I$: Set of months, $i \in I$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $num_m$: Number of machines
    \item $profit_k$: Profit per unit of product $k$
    \item $time_{k,m}$: Time required to produce product $k$ on machine $m$ (hours)
    \item $down_m$: Maintenance downtime for machine $m$ (months)
    \item $limit_{k,i}$: Marketing limitation for product $k$ in month $i$
    \item $store\_price$: Cost of storing each product per unit per month
    \item $keep\_quantity$: Desired stock level for each product at the end of each month
    \item $n\_workhours$: Total working hours in a month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Amount of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Amount of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Amount of product $k$ stored at the end of month $i$
    \item $maintain_{m,k}$: Number of machines maintained for product $k$ in month $i$
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize} \quad Z = \sum_{i \in I} \sum_{k \in K} profit_k \cdot sell_{k,i} - \sum_{i \in I} \sum_{k \in K} store\_price \cdot storage_{k,i}
\]

\subsection*{Constraints}

\subsubsection*{Production Time Constraint}
For each product $k$ in month $i$, the total production time should not exceed available working hours:
\[
\sum_{m \in M} time_{k,m} \cdot manufacture_{k,i} \leq n\_workhours \cdot (1 - \sum_{m \in M} maintain_{m,k})
\]
For a machine $m$ that is down for maintenance:
\[
maintain_{m,k} \leq down_m
\]

\subsubsection*{Marketing Limitations}
The amount sold cannot exceed marketing limitations:
\[
sell_{k,i} \leq limit_{k,i}
\]

\subsubsection*{Storage Constraints}
The storage at the end of month $i$ must account for manufactured products and sales:
\[
storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i}
\]
With the condition:
\[
storage_{k,i} \leq 100
\]

\subsubsection*{Ending Stock Requirement}
At the end of each month, the storage must meet the desired quantity:
\[
storage_{k,I} \geq keep\_quantity
\]

\subsubsection*{Non-negativity and Integrality Constraints}
\[
manufacture_{k,i} \geq 0, \quad sell_{k,i} \geq 0, \quad storage_{k,i} \geq 0, \quad maintain_{m,k} \in \{0, 1\}
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

\section*{Mixed Integer Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item $M$: Set of machines, $m \in M$
    \item $K$: Set of products, $k \in K$
    \item $I$: Set of months, $i \in I$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $num_m$: Number of machines
    \item $profit_k$: Profit per unit of product $k$
    \item $time_{k,m}$: Time required to produce product $k$ on machine $m$ (hours)
    \item $down_m$: Maintenance downtime for machine $m$ (months)
    \item $limit_{k,i}$: Marketing limitation for product $k$ in month $i$
    \item $store\_price$: Cost of storing each product per unit per month
    \item $keep\_quantity$: Desired stock level for each product at the end of each month
    \item $n\_workhours$: Total working hours in a month
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Amount of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Amount of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Amount of product $k$ stored at the end of month $i$
    \item $maintain_{m,k}$: Number of machines maintained for product $k$ in month $i$
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize} \quad Z = \sum_{i \in I} \sum_{k \in K} profit_k \cdot sell_{k,i} - \sum_{i \in I} \sum_{k \in K} store\_price \cdot storage_{k,i}
\]

\subsection*{Constraints}

\subsubsection*{Production Time Constraint}
For each product $k$ in month $i$, the total production time should not exceed available working hours:
\[
\sum_{m \in M} time_{k,m} \cdot manufacture_{k,i} \leq n\_workhours \cdot (1 - \sum_{m \in M} maintain_{m,k})
\]
For a machine $m$ that is down for maintenance:
\[
maintain_{m,k} \leq down_m
\]

\subsubsection*{Marketing Limitations}
The amount sold cannot exceed marketing limitations:
\[
sell_{k,i} \leq limit_{k,i}
\]

\subsubsection*{Storage Constraints}
The storage at the end of month $i$ must account for manufactured products and sales:
\[
storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i}
\]
With the condition:
\[
storage_{k,i} \leq 100
\]

\subsubsection*{Ending Stock Requirement}
At the end of each month, the storage must meet the desired quantity:
\[
storage_{k,I} \geq keep\_quantity
\]

\subsubsection*{Non-negativity and Integrality Constraints}
\[
manufacture_{k,i} \geq 0, \quad sell_{k,i} \geq 0, \quad storage_{k,i} \geq 0, \quad maintain_{m,k} \in \{0, 1\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
    'down': [[0, 1, 1, 1, 1]], 
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]], 
    'store_price': 0.5, 
    'keep_quantity': 100, 
    'n_workhours': 8.0
}

#### Sets
M = range(len(data['num_machines']))  #### machines
K = range(len(data['profit']))         #### products
I = range(len(data['limit'][0]))       #### months

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, K), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in K for i in I) - pulp.lpSum(data['store_price'] * storage[k][i] for k in K for i in I)

#### Constraints
#### Production Time Constraint
for k in K:
    for i in I:
        problem += (pulp.lpSum(data['time[i][m]'] * manufacture[k][i] for m in M) <= 
                     data['n_workhours'] * (1 - pulp.lpSum(maintain[m][k] for m in M)), f"Production_Time_Constraint_k{str(k)}_i{str(i)}")

#### Maintenance Constraint
for m in M:
    for k in K:
        problem += maintain[m][k] <= data['down'][0][m], f"Maintenance_Constraint_m{str(m)}_k{str(k)}"

#### Marketing Limitations
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i], f"Marketing_Limitations_k{str(k)}_i{str(i)}"

#### Storage Constraints
for k in K:
    for i in range(1, len(I)):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i],
                     f"Storage_Constraint_k{str(k)}_i{str(i)}")
        problem += storage[k][i] <= 100, f"Storage_Limit_k{str(k)}_i{str(i)}"

#### Ending Stock Requirement
for k in K:
    problem += storage[k][len(I)-1] >= data['keep_quantity'], f"Ending_Stock_Requirement_k{str(k)}"

#### Solve the problem
problem.solve()

#### Print the objective value
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

#### Data from JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
    'down': [[0, 1, 1, 1, 1]], 
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]], 
    'store_price': 0.5, 
    'keep_quantity': 100, 
    'n_workhours': 8.0
}

#### Sets
M = range(len(data['num_machines']))  #### machines
K = range(len(data['profit']))         #### products
I = range(len(data['limit'][0]))       #### months

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, K), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in K for i in I) - pulp.lpSum(data['store_price'] * storage[k][i] for k in K for i in I)

#### Constraints
#### Production Time Constraint
for k in K:
    for i in I:
        problem += (pulp.lpSum(data['time[i][m]'] * manufacture[k][i] for m in M) <= 
                     data['n_workhours'] * (1 - pulp.lpSum(maintain[m][k] for m in M)), f"Production_Time_Constraint_k{str(k)}_i{str(i)}")

#### Maintenance Constraint
for m in M:
    for k in K:
        problem += maintain[m][k] <= data['down'][0][m], f"Maintenance_Constraint_m{str(m)}_k{str(k)}"

#### Marketing Limitations
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i], f"Marketing_Limitations_k{str(k)}_i{str(i)}"

#### Storage Constraints
for k in K:
    for i in range(1, len(I)):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i],
                     f"Storage_Constraint_k{str(k)}_i{str(i)}")
        problem += storage[k][i] <= 100, f"Storage_Limit_k{str(k)}_i{str(i)}"

#### Ending Stock Requirement
for k in K:
    problem += storage[k][len(I)-1] >= data['keep_quantity'], f"Ending_Stock_Requirement_k{str(k)}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/3/21/python_code0.py", line 48, in <module>
    problem += (pulp.lpSum(data['time[i][m]'] * manufacture[k][i] for m in M) <= 
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/3/21/python_code0.py", line 48, in <genexpr>
    problem += (pulp.lpSum(data['time[i][m]'] * manufacture[k][i] for m in M) <= 
                           ~~~~^^^^^^^^^^^^^^
KeyError: 'time[i][m]'
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
    'down': [[0, 1, 1, 1, 1]], 
    'limit': [[500, 600, 300, 200, 0, 500], 
              [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], 
              [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], 
              [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]], 
    'store_price': 0.5, 
    'keep_quantity': 100, 
    'n_workhours': 8.0
}

#### Sets
M = range(len(data['num_machines']))  #### machines
K = range(len(data['profit']))         #### products
I = range(len(data['limit'][0]))       #### months

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, K), cat='Binary')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in K for i in I) - pulp.lpSum(data['store_price'] * storage[k][i] for k in K for i in I)

#### Constraints
#### Production Time Constraint
for k in K:
    for i in I:
        problem += (pulp.lpSum(data['time'][i][m] * manufacture[k][i] for m in M) <= 
                     data['n_workhours'] * (1 - pulp.lpSum(maintain[m][k] for m in M)), f"Production_Time_Constraint_k{str(k)}_i{str(i)}")

#### Maintenance Constraint
for m in M:
    for k in K:
        problem += maintain[m][k] <= data['down'][0][m], f"Maintenance_Constraint_m{str(m)}_k{str(k)}"

#### Marketing Limitations
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i], f"Marketing_Limitations_k{str(k)}_i{str(i)}"

#### Storage Constraints
for k in K:
    for i in range(1, len(I)):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i],
                     f"Storage_Constraint_k{str(k)}_i{str(i)}")
        problem += storage[k][i] <= 100, f"Storage_Limit_k{str(k)}_i{str(i)}"

#### Ending Stock Requirement
for k in K:
    problem += storage[k][len(I)-1] >= data['keep_quantity'], f"Ending_Stock_Requirement_k{str(k)}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

