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

\section*{Mathematical Model for Engineering Factory Problem}

\subsection*{Sets}
\begin{itemize}
    \item $M$: Set of machines, $m = 1, \ldots, M$
    \item $K$: Set of products, $k = 1, \ldots, K$
    \item $I$: Set of months, $i = 1, \ldots, I$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $num_m$: Number of machines
    \item $profit_k$: Profit from selling product $k$
    \item $time_{k,m}$: Production time of product $k$ on machine $m$
    \item $down_m$: Number of months machine $m$ is down for maintenance
    \item $limit_{k,i}$: Marketing limitation of product $k$ in month $i$
    \item $store\_price$: Cost of storing one unit of product per month
    \item $keep\_quantity$: Desired quantity of each product at the end of subsequent months
    \item $n\_workhours$: Number of working hours per day
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Quantity of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Quantity of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Quantity of product $k$ stored at the end of month $i$
    \item $maintain_{m,i}$: Number of machines in maintenance in month $i$ for each type $m$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_k \cdot sell_{k,i} - \sum_{k=1}^{K} \sum_{i=1}^{I} store\_price \cdot storage_{k,i}
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Production Time Constraint:}
    \[
    \sum_{k=1}^{K} time_{k,m} \cdot manufacture_{k,i} \leq n\_workhours \cdot (6 \text{ days}) \cdot (24 \text{ hours}) - \sum_{j=1}^{down_m} maintain_{m,i+j}
    \]
    for each machine $m$ and month $i$.

    \item \textbf{Storage Constraint:}
    \[
    storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} \quad \forall k, \forall i
    \]
    with $storage_{k,0} = 0$ (initial stock).

    \item \textbf{Marketing Limitations:}
    \[
    sell_{k,i} \leq limit_{k,i} \quad \forall k, \forall i
    \]

    \item \textbf{Desired End-of-Month Stock:}
    \[
    storage_{k,I} \geq keep\_quantity \quad \forall k
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0, \quad maintain_{m,i} \geq 0 \quad \forall k, m, i
    \]
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

\section*{Mathematical Model for Engineering Factory Problem}

\subsection*{Sets}
\begin{itemize}
    \item $M$: Set of machines, $m = 1, \ldots, M$
    \item $K$: Set of products, $k = 1, \ldots, K$
    \item $I$: Set of months, $i = 1, \ldots, I$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $num_m$: Number of machines
    \item $profit_k$: Profit from selling product $k$
    \item $time_{k,m}$: Production time of product $k$ on machine $m$
    \item $down_m$: Number of months machine $m$ is down for maintenance
    \item $limit_{k,i}$: Marketing limitation of product $k$ in month $i$
    \item $store\_price$: Cost of storing one unit of product per month
    \item $keep\_quantity$: Desired quantity of each product at the end of subsequent months
    \item $n\_workhours$: Number of working hours per day
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Quantity of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Quantity of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Quantity of product $k$ stored at the end of month $i$
    \item $maintain_{m,i}$: Number of machines in maintenance in month $i$ for each type $m$
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} profit_k \cdot sell_{k,i} - \sum_{k=1}^{K} \sum_{i=1}^{I} store\_price \cdot storage_{k,i}
\]

\subsection*{Constraints}

\begin{itemize}
    \item \textbf{Production Time Constraint:}
    \[
    \sum_{k=1}^{K} time_{k,m} \cdot manufacture_{k,i} \leq n\_workhours \cdot (6 \text{ days}) \cdot (24 \text{ hours}) - \sum_{j=1}^{down_m} maintain_{m,i+j}
    \]
    for each machine $m$ and month $i$.

    \item \textbf{Storage Constraint:}
    \[
    storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} \quad \forall k, \forall i
    \]
    with $storage_{k,0} = 0$ (initial stock).

    \item \textbf{Marketing Limitations:}
    \[
    sell_{k,i} \leq limit_{k,i} \quad \forall k, \forall i
    \]

    \item \textbf{Desired End-of-Month Stock:}
    \[
    storage_{k,I} \geq keep\_quantity \quad \forall k
    \]

    \item \textbf{Non-negativity Constraints:}
    \[
    sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0, \quad maintain_{m,i} \geq 0 \quad \forall k, m, i
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = {'num_machines': [4, 2, 3, 1, 1], 
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
        'n_workhours': 8.0}

#### Constants
num_m = len(data['num_machines'])  #### Number of machines
num_k = len(data['profit'])         #### Number of products
num_i = len(data['limit'][0])       #### Number of months

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_k), range(num_i)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_k), range(num_i)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_k), range(num_i)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_m), range(num_i)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_k) for i in range(num_i)) \
           - pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_k) for i in range(num_i))

#### Constraints
#### Production Time Constraint
for m in range(num_m):
    for i in range(num_i):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_k)) \
                   <= data['n_workhours'] * 6 * 24 - pulp.lpSum(maintain[m][i+j] for j in range(data['down'][0][m]))

#### Storage Constraint
for k in range(num_k):
    for i in range(1, num_i):  #### Start from month 1
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

#### Set initial storage
for k in range(num_k):
    problem += storage[k][0] == 0  #### Initial stock

#### Marketing Limitations
for k in range(num_k):
    for i in range(num_i):
        problem += sell[k][i] <= data['limit'][k][i]

#### Desired End-of-Month Stock
for k in range(num_k):
    problem += storage[k][num_i-1] >= data['keep_quantity']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

