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
To model the given problem as a Mixed Integer Linear Programming (MILP) problem, we'll define decision variables, constraints, and an objective function to optimize (maximize the profit). Here's the mathematical model represented in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Indices}
\begin{align*}
    & k \quad \text{Index for products,} \quad k = 1, \ldots, K \\
    & i \quad \text{Index for months,} \quad i = 1, \ldots, I \\
    & m \quad \text{Index for machines,} \quad m = 1, \ldots, M \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & \text{num}_{m} \quad \text{Number of machines of type } m \\
    & \text{profit}_{k} \quad \text{Profit per unit of product } k \\
    & \text{time}_{k,m} \quad \text{Time required to produce product } k \text{ on machine } m \\
    & \text{down}_{m} \quad \text{Number of months machine } m \text{ is down for maintenance} \\
    & \text{limit}_{k,i} \quad \text{Marketing limitation of product } k \text{ in month } i \\
    & \text{store\_price} \quad \text{Storage cost per unit per month} \\
    & \text{keep\_quantity} \quad \text{Desired stock of each product at the end of the planning period} \\
    & \text{n\_workhours} \quad \text{Working hours per shift per day} \\
    & \text{Working days per month (assumed)} = 24 \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{sell}_{k,i} \quad \text{Units of product } k \text{ sold in month } i \\
    & \text{manufacture}_{k,i} \quad \text{Units of product } k \text{ manufactured in month } i \\
    & \text{storage}_{k,i} \quad \text{Units of product } k \text{ stored at the end of month } i \\
    & \text{maintain}_{m,i} \quad \text{Number of machine type } m \text{ under maintenance in month } i \\
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\begin{align*}
    \max \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_{k} \times \text{sell}_{k,i} - \text{store\_price} \times \text{storage}_{k,i} \right)
\end{align*}

\subsection*{Constraints}

\subsubsection*{Manufacturing and Sales Constraints}
\begin{align*}
    \text{manufacture}_{k,i} &= \text{sell}_{k,i} + \text{storage}_{k,i-1} - \text{storage}_{k,i}, \quad \forall k, \forall i \\
    \text{storage}_{k,0} &= 0, \quad \forall k
\end{align*}

\subsubsection*{Machine Time Constraints}
\begin{align*}
    \sum_{k=1}^{K} \text{manufacture}_{k,i} \times \text{time}_{k,m} &\leq \left( \text{num}_{m} - \text{maintain}_{m,i} \right) \times 24 \times 2 \times \text{n\_workhours}, \quad \forall m, \forall i
\end{align*}

\subsubsection*{Maintenance Constraints}
\begin{align*}
    \sum_{i=1}^{I} \text{maintain}_{m,i} &= \text{down}_{m}, \quad \forall m
\end{align*}

\subsubsection*{Marketing Limitation Constraints}
\begin{align*}
    \text{sell}_{k,i} &\leq \text{limit}_{k,i}, \quad \forall k, \forall i
\end{align*}

\subsubsection*{Storage Capacity Constraints}
\begin{align*}
    \text{storage}_{k,i} &\leq 100, \quad \forall k, \forall i
\end{align*}

\subsubsection*{Final Stock Requirement}
\begin{align*}
    \text{storage}_{k,I} &= \text{keep\_quantity}, \quad \forall k
\end{align*}

\subsubsection*{Non-negativity Constraints}
\begin{align*}
    & \text{sell}_{k,i}, \text{manufacture}_{k,i}, \text{storage}_{k,i} \geq 0, \quad \forall k, \forall i \\
    & \text{maintain}_{m,i} \geq 0, \quad \forall m, \forall i
\end{align*}

\end{document}
```

This LaTeX code represents the MILP formulation for the given problem, including objective function and constraints. You can compile it using any LaTeX editor to generate a readable format.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Indices}
\begin{align*}
    & k \quad \text{Index for products,} \quad k = 1, \ldots, K \\
    & i \quad \text{Index for months,} \quad i = 1, \ldots, I \\
    & m \quad \text{Index for machines,} \quad m = 1, \ldots, M \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
    & \text{num}_{m} \quad \text{Number of machines of type } m \\
    & \text{profit}_{k} \quad \text{Profit per unit of product } k \\
    & \text{time}_{k,m} \quad \text{Time required to produce product } k \text{ on machine } m \\
    & \text{down}_{m} \quad \text{Number of months machine } m \text{ is down for maintenance} \\
    & \text{limit}_{k,i} \quad \text{Marketing limitation of product } k \text{ in month } i \\
    & \text{store\_price} \quad \text{Storage cost per unit per month} \\
    & \text{keep\_quantity} \quad \text{Desired stock of each product at the end of the planning period} \\
    & \text{n\_workhours} \quad \text{Working hours per shift per day} \\
    & \text{Working days per month (assumed)} = 24 \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{sell}_{k,i} \quad \text{Units of product } k \text{ sold in month } i \\
    & \text{manufacture}_{k,i} \quad \text{Units of product } k \text{ manufactured in month } i \\
    & \text{storage}_{k,i} \quad \text{Units of product } k \text{ stored at the end of month } i \\
    & \text{maintain}_{m,i} \quad \text{Number of machine type } m \text{ under maintenance in month } i \\
\end{align*}

\subsection*{Objective Function}
Maximize total profit:
\begin{align*}
    \max \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_{k} \times \text{sell}_{k,i} - \text{store\_price} \times \text{storage}_{k,i} \right)
\end{align*}

\subsection*{Constraints}

\subsubsection*{Manufacturing and Sales Constraints}
\begin{align*}
    \text{manufacture}_{k,i} &= \text{sell}_{k,i} + \text{storage}_{k,i-1} - \text{storage}_{k,i}, \quad \forall k, \forall i \\
    \text{storage}_{k,0} &= 0, \quad \forall k
\end{align*}

\subsubsection*{Machine Time Constraints}
\begin{align*}
    \sum_{k=1}^{K} \text{manufacture}_{k,i} \times \text{time}_{k,m} &\leq \left( \text{num}_{m} - \text{maintain}_{m,i} \right) \times 24 \times 2 \times \text{n\_workhours}, \quad \forall m, \forall i
\end{align*}

\subsubsection*{Maintenance Constraints}
\begin{align*}
    \sum_{i=1}^{I} \text{maintain}_{m,i} &= \text{down}_{m}, \quad \forall m
\end{align*}

\subsubsection*{Marketing Limitation Constraints}
\begin{align*}
    \text{sell}_{k,i} &\leq \text{limit}_{k,i}, \quad \forall k, \forall i
\end{align*}

\subsubsection*{Storage Capacity Constraints}
\begin{align*}
    \text{storage}_{k,i} &\leq 100, \quad \forall k, \forall i
\end{align*}

\subsubsection*{Final Stock Requirement}
\begin{align*}
    \text{storage}_{k,I} &= \text{keep\_quantity}, \quad \forall k
\end{align*}

\subsubsection*{Non-negativity Constraints}
\begin{align*}
    & \text{sell}_{k,i}, \text{manufacture}_{k,i}, \text{storage}_{k,i} \geq 0, \quad \forall k, \forall i \\
    & \text{maintain}_{m,i} \geq 0, \quad \forall m, \forall i
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
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
        [0.0, 0.0, 0.0, 0.2, 0.01]
    ],
    'down': [0, 1, 1, 1, 1],
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

K = len(data['profit'])     #### Number of products
I = len(data['limit'][0])   #### Number of months
M = len(data['num_machines'])  #### Number of machine types

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I))

#### Constraints

#### Manufacturing and Sales Constraints
for k in range(K):
    problem += (storage[k, 0] == 0)
    for i in range(I):
        if i == 0:
            problem += (manufacture[k, i] == sell[k, i] + 0 - storage[k, i])
        else:
            problem += (manufacture[k, i] == sell[k, i] + storage[k, i - 1] - storage[k, i])

#### Machine Time Constraints
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(manufacture[k, i] * data['time'][k][m] for k in range(K)) <= 
                    (data['num_machines'][m] - maintain[m, i]) * 24 * 2 * data['n_workhours'])

#### Maintenance Constraints
for m in range(M):
    problem += (pulp.lpSum(maintain[m, i] for i in range(I)) == data['down'][m])

#### Marketing Limitation Constraints
for k in range(K):
    for i in range(I):
        problem += (sell[k, i] <= data['limit'][k][i])

#### Storage Capacity Constraints
for k in range(K):
    for i in range(I):
        problem += (storage[k, i] <= 100)

#### Final Stock Requirement
for k in range(K):
    problem += (storage[k, I - 1] == data['keep_quantity'])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

