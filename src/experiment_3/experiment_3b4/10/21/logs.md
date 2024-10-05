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
The given problem is a Mixed-Integer Linear Programming (MILP) problem. Let's construct the mathematical model for this scenario.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

Given:
\begin{itemize}
    \item \( M \): Number of machine types.
    \item \( K \): Number of products.
    \item \( I \): Number of months.
    \item \( \text{num}_m \): Number of machines for each type \( m \).
    \item \( \text{profit}_k \): Profit per unit for product \( k \).
    \item \( \text{time}_{k,m} \): Production time required for product \( k \) on machine \( m \).
    \item \( \text{down}_m \): Number of months machine \( m \) is down for maintenance.
    \item \( \text{limit}_{k,i} \): Maximum amount of product \( k \) that can be sold in month \( i \).
    \item \( \text{store\_price} \): Storage cost per unit per month.
    \item \( \text{keep\_quantity} \): Desired stock of each type of product at the end.
    \item \( \text{n\_workhours} \): Number of work hours per shift.
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    \text{sell}_{k,i} & : \text{Quantity of product } k \text{ sold in month } i. \\
    \text{manufacture}_{k,i} & : \text{Quantity of product } k \text{ manufactured in month } i. \\
    \text{storage}_{k,i} & : \text{Quantity of product } k \text{ stored at the end of month } i. \\
    \text{maintain}_{m,i} & : \text{Number of machines of type } m \text{ under maintenance in month } i.
\end{align*}

\textbf{Objective Function:}
\[
    \max \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \times \text{sell}_{k,i} - \text{store\_price} \times \text{storage}_{k,i} \right)
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Balance constraint for products:} \\
    & \quad \text{storage}_{k,i} = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i}, \quad \forall k, \; \forall i \\
    & \quad \text{where } \text{storage}_{k,0} = 0 \text{ (initial stock)} \\
    & \text{Sales limit:} \\
    & \quad \text{sell}_{k,i} \leq \text{limit}_{k,i}, \quad \forall k, \; \forall i \\
    & \text{Storage limit:} \\
    & \quad \text{storage}_{k,i} \leq 100, \quad \forall k, \; \forall i \\
    & \text{End stock requirement:} \\
    & \quad \text{storage}_{k,I} = \text{keep\_quantity}, \quad \forall k \\
    & \text{Machine availability constraint:} \\
    & \quad \sum_{k=1}^{K} \text{time}_{k,m} \times \text{manufacture}_{k,i} \leq \left(\text{num}_m - \text{maintain}_{m,i}\right) \times 24 \times 6 \times \text{n\_workhours}, \quad \forall m, \; \forall i \\
    & \text{Maintenance constraint:} \\
    & \quad \sum_{i=1}^{I} \text{maintain}_{m,i} = \text{down}_m, \quad \forall m
\end{align*}

All decision variables are non-negative integers.

\end{document}
```

This model maximizes the profit by considering the selling, manufacturing, storing, and maintaining constraints over the specified period. The constraints ensure that the production does not exceed machine capacity, the sales do not exceed marketing limits, and desired end-of-period stocks are maintained.

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

Given:
\begin{itemize}
    \item \( M \): Number of machine types.
    \item \( K \): Number of products.
    \item \( I \): Number of months.
    \item \( \text{num}_m \): Number of machines for each type \( m \).
    \item \( \text{profit}_k \): Profit per unit for product \( k \).
    \item \( \text{time}_{k,m} \): Production time required for product \( k \) on machine \( m \).
    \item \( \text{down}_m \): Number of months machine \( m \) is down for maintenance.
    \item \( \text{limit}_{k,i} \): Maximum amount of product \( k \) that can be sold in month \( i \).
    \item \( \text{store\_price} \): Storage cost per unit per month.
    \item \( \text{keep\_quantity} \): Desired stock of each type of product at the end.
    \item \( \text{n\_workhours} \): Number of work hours per shift.
\end{itemize}

\textbf{Decision Variables:}
\begin{align*}
    \text{sell}_{k,i} & : \text{Quantity of product } k \text{ sold in month } i. \\
    \text{manufacture}_{k,i} & : \text{Quantity of product } k \text{ manufactured in month } i. \\
    \text{storage}_{k,i} & : \text{Quantity of product } k \text{ stored at the end of month } i. \\
    \text{maintain}_{m,i} & : \text{Number of machines of type } m \text{ under maintenance in month } i.
\end{align*}

\textbf{Objective Function:}
\[
    \max \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \times \text{sell}_{k,i} - \text{store\_price} \times \text{storage}_{k,i} \right)
\]

\textbf{Constraints:}
\begin{align*}
    & \text{Balance constraint for products:} \\
    & \quad \text{storage}_{k,i} = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i}, \quad \forall k, \; \forall i \\
    & \quad \text{where } \text{storage}_{k,0} = 0 \text{ (initial stock)} \\
    & \text{Sales limit:} \\
    & \quad \text{sell}_{k,i} \leq \text{limit}_{k,i}, \quad \forall k, \; \forall i \\
    & \text{Storage limit:} \\
    & \quad \text{storage}_{k,i} \leq 100, \quad \forall k, \; \forall i \\
    & \text{End stock requirement:} \\
    & \quad \text{storage}_{k,I} = \text{keep\_quantity}, \quad \forall k \\
    & \text{Machine availability constraint:} \\
    & \quad \sum_{k=1}^{K} \text{time}_{k,m} \times \text{manufacture}_{k,i} \leq \left(\text{num}_m - \text{maintain}_{m,i}\right) \times 24 \times 6 \times \text{n\_workhours}, \quad \forall m, \; \forall i \\
    & \text{Maintenance constraint:} \\
    & \quad \sum_{i=1}^{I} \text{maintain}_{m,i} = \text{down}_m, \quad \forall m
\end{align*}

All decision variables are non-negative integers.

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [
    [0.5, 0.1, 0.2, 0.05, 0.0],
    [0.7, 0.2, 0.0, 0.03, 0.0],
    [0.0, 0.0, 0.8, 0.0, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.0],
    [0.3, 0.0, 0.0, 0.1, 0.05],
    [0.5, 0.0, 0.6, 0.08, 0.05],
    [0.0, 0.0, 0.0, 0.0, 0.05]
]
down = [0, 1, 1, 1, 1]
limit = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0

M = len(num_machines)
K = len(profit)
I = len(limit[0])

#### Problem
problem = pulp.LpProblem("Manufacturing_Optimization", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("Sell", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpInteger)
manufacture = pulp.LpVariable.dicts("Manufacture", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", [(k, i) for k in range(K) for i in range(I)], lowBound=0, upBound=100, cat=pulp.LpInteger)
maintain = pulp.LpVariable.dicts("Maintain", [(m, i) for m in range(M) for i in range(I)], lowBound=0, cat=pulp.LpInteger)

#### Objective Function
profit_term = pulp.lpSum(profit[k] * sell[k, i] for k in range(K) for i in range(I))
storage_cost_term = pulp.lpSum(store_price * storage[k, i] for k in range(K) for i in range(I))
problem += profit_term - storage_cost_term

#### Constraints
for k in range(K):
    #### Storage balance for each product
    problem += storage[k, 0] == manufacture[k, 0] - sell[k, 0]
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]
    #### End stock requirement
    problem += storage[k, I-1] == keep_quantity

    #### Sales limits
    for i in range(I):
        problem += sell[k, i] <= limit[k][i]

#### Machine availability constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= (num_machines[m] - maintain[m, i]) * 24 * 6 * n_workhours

    #### Maintenance constraints
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

