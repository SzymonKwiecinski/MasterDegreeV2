# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- An engineering factory makes several products on the machines, and the number of machine \var{m} the factory has is \var{num_{m}}.
- Each product \var{k} yields \var{profit_{k}} to profit (defined as £/unit selling price minus cost of raw materials).
- The unit production times (hours) product \var{k} requires on machine \var{m} is \var{time_{k, m}}
- In the present month (January) and several subsequent months, certain machines will be down for maintenance.
- In month \var{i}, the number of machine \var{m} that will be down is \var{maintain_{i, m}}.
- There are marketing limitations on each product in each month. 
- The limitation of product \var{k} in month \var{i} is \var{limit_{k, i}}.
- It is possible to store up to 100 of each product at a time at a cost of \var{store_price} per unit per month. 
- There are no stocks at present, but we should have a stock of \var{keep_quantity} of each type of product at the end of subsequent months.
- The factory works six days a week with \var{n_workhours} hours each day. 
- No sequencing problems need to be considered.
- We can assume that a month has 24 days for convenience.

INPUT FORMAT:

{
    "num_machines": [num_{m} for m in 1,...,M],
    "profit": [profit_{k} for k in 1,...K],
    "time": [[time_{k, m} for m in 1,...,M] for k in 1,...,K],
    "maintain": [[maintain_{i, m} for m in 1,...,M] for i in 1,...,I],
    "limit": [[limit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "store_price": store_price,
    "keep_quantity": keep_quantity,
    "n_workhours": n_workhours
}

OBJECTIVE: What selling, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO:

- \var{sell} represents the amount of selling quantity of each product in each month
- \var{manufacture} represents the amount of manufactured products in each month
- \var{storage} represents the storage of each product in each month

OUTPUT FORMAT:

{
    "sell": [[sell_{k, i} for k in 1,...,K] for i in 1,...I],
    "manufacture": [[manufacture_{k, i} for k in 1,...,K] for i in 1,...I],
    "storage": [[storage_{k, i} for k in 1,...,K] for i in 1,...,I]
}

</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of machines
    \item $K$: Number of products
    \item $I$: Number of months
    \item $num_m$: Total number of machines, where $m = 1, \ldots, M$
    \item $profit_k$: Profit earned from selling one unit of product $k$, where $k = 1, \ldots, K$
    \item $time_{k,m}$: Time required to produce one unit of product $k$ on machine $m$
    \item $maintain_{i,m}$: Number of machines down for maintenance in month $i$, where $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $limit_{k,i}$: Marketing limitation for product $k$ in month $i$
    \item $store\_price$: Cost of storage per unit of product per month
    \item $keep\_quantity$: Desired stock level of each product at the end of each month
    \item $n\_workhours$: Number of work hours per day
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Quantity of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Quantity of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Quantity of product $k$ stored at the end of month $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} (profit_k \cdot sell_{k,i} - store\_price \cdot storage_{k,i})
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production time constraint:
    \[
    \sum_{k=1}^{K} \sum_{m=1}^{M} time_{k,m} \cdot manufacture_{k,i} \leq (n\_workhours \cdot 6 \cdot 24 - \sum_{m=1}^{M} maintain_{i,m}) \quad \forall i
    \]
    
    \item Marketing limitation:
    \[
    sell_{k,i} \leq limit_{k,i} \quad \forall k, \forall i
    \]

    \item Storage constraint:
    \[
    storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} \quad \forall k, \forall i
    \]
    
    \item End-of-month inventory constraint:
    \[
    storage_{k,I} \geq keep\_quantity \quad \forall k
    \]
    
    \item Non-negativity constraints:
    \[
    sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0 \quad \forall k, \forall i
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

\section*{Linear Programming Model}

\subsection*{Parameters}
\begin{itemize}
    \item $M$: Number of machines
    \item $K$: Number of products
    \item $I$: Number of months
    \item $num_m$: Total number of machines, where $m = 1, \ldots, M$
    \item $profit_k$: Profit earned from selling one unit of product $k$, where $k = 1, \ldots, K$
    \item $time_{k,m}$: Time required to produce one unit of product $k$ on machine $m$
    \item $maintain_{i,m}$: Number of machines down for maintenance in month $i$, where $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $limit_{k,i}$: Marketing limitation for product $k$ in month $i$
    \item $store\_price$: Cost of storage per unit of product per month
    \item $keep\_quantity$: Desired stock level of each product at the end of each month
    \item $n\_workhours$: Number of work hours per day
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $sell_{k,i}$: Quantity of product $k$ sold in month $i$
    \item $manufacture_{k,i}$: Quantity of product $k$ manufactured in month $i$
    \item $storage_{k,i}$: Quantity of product $k$ stored at the end of month $i$
\end{itemize}

\subsection*{Objective Function}
The objective is to maximize total profit:
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} (profit_k \cdot sell_{k,i} - store\_price \cdot storage_{k,i})
\]

\subsection*{Constraints}
\begin{itemize}
    \item Production time constraint:
    \[
    \sum_{k=1}^{K} \sum_{m=1}^{M} time_{k,m} \cdot manufacture_{k,i} \leq (n\_workhours \cdot 6 \cdot 24 - \sum_{m=1}^{M} maintain_{i,m}) \quad \forall i
    \]
    
    \item Marketing limitation:
    \[
    sell_{k,i} \leq limit_{k,i} \quad \forall k, \forall i
    \]

    \item Storage constraint:
    \[
    storage_{k,i} = storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} \quad \forall k, \forall i
    \]
    
    \item End-of-month inventory constraint:
    \[
    storage_{k,I} \geq keep\_quantity \quad \forall k
    \]
    
    \item Non-negativity constraints:
    \[
    sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0 \quad \forall k, \forall i
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

#### Parameters
M = len(data['num_machines'])  #### Number of machines
K = len(data['profit'])         #### Number of products
I = len(data['limit'])          #### Number of months
profit_k = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(profit_k[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I)), "Total_Profit"

#### Constraints

#### Production time constraint
for i in range(I):
    problem += (
        pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) for m in range(M)) 
        <= (n_workhours * 6 * 24 - pulp.lpSum(maintain[i][m] for m in range(M))),
        f"Production_Time_Constraint_{i}"
    )

#### Marketing limitation
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[i][k], f"Marketing_Limit_{k}_{i}"

#### Storage constraint
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Constraint_{k}_{i}"

#### End-of-month inventory constraint
for k in range(K):
    problem += storage[k][I-1] >= keep_quantity, f"End_Inventory_Constraint_{k}"

#### Non-negativity constraints (already incorporated with lowBound=0)

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

