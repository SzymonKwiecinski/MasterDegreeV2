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

\section*{Linear Programming Model for Maximizing Profit in an Engineering Factory}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of machines, \( K \) be the number of products, and \( I \) be the number of months.
    \item \( \text{num}_m \) is the number of machines.
    \item \( \text{profit}_k \) is the profit from selling product \( k \).
    \item \( \text{time}_{k, m} \) is the production time of product \( k \) on machine \( m \) (in hours).
    \item \( \text{maintain}_{i, m} \) is the number of machines down for maintenance in month \( i \).
    \item \( \text{limit}_{k, i} \) is the marketing limit for product \( k \) in month \( i \).
    \item \( \text{store\_price} \) is the cost of storing one unit of product per month.
    \item \( \text{keep\_quantity} \) is the desired inventory amount of each product at the end of each month.
    \item \( n_{\text{workhours}} \) is the number of work hours per day multiplied by 6 days a week during a month.
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( \text{sell}_{k, i} \) be the quantity of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k, i} \) be the quantity of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k, i} \) be the quantity of product \( k \) stored at the end of month \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \cdot \text{sell}_{k, i} - \text{store\_price} \cdot \text{storage}_{k, i} \right)
\]

\subsection*{Constraints}
1. **Production Time Constraint**:
   \[
   \sum_{k=1}^{K} \sum_{m=1}^{M} \text{time}_{k, m} \cdot \text{manufacture}_{k, i} \leq n_{\text{workhours}} \cdot \left( \text{num}_m - \sum_{m=1}^{M} \text{maintain}_{i, m} \right) \quad \forall i
   \]

2. **Marketing Limitation**:
   \[
   \text{sell}_{k, i} \leq \text{limit}_{k, i} \quad \forall k, \forall i
   \]

3. **Storage Constraints**:
   \[
   \text{storage}_{k, i} = \text{storage}_{k, i-1} + \text{manufacture}_{k, i} - \text{sell}_{k, i} \quad \forall k, \forall i \; (i > 1)
   \]
   \[
   \text{storage}_{k, 1} = 0 \quad \forall k
   \]

4. **Ending Inventory Requirement**:
   \[
   \text{storage}_{k, I} \geq \text{keep\_quantity} \quad \forall k
   \]

5. **Non-negativity Constraints**:
   \[
   \text{sell}_{k, i} \geq 0, \quad \text{manufacture}_{k, i} \geq 0, \quad \text{storage}_{k, i} \geq 0 \quad \forall k, i
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

\section*{Linear Programming Model for Maximizing Profit in an Engineering Factory}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the number of machines, \( K \) be the number of products, and \( I \) be the number of months.
    \item \( \text{num}_m \) is the number of machines.
    \item \( \text{profit}_k \) is the profit from selling product \( k \).
    \item \( \text{time}_{k, m} \) is the production time of product \( k \) on machine \( m \) (in hours).
    \item \( \text{maintain}_{i, m} \) is the number of machines down for maintenance in month \( i \).
    \item \( \text{limit}_{k, i} \) is the marketing limit for product \( k \) in month \( i \).
    \item \( \text{store\_price} \) is the cost of storing one unit of product per month.
    \item \( \text{keep\_quantity} \) is the desired inventory amount of each product at the end of each month.
    \item \( n_{\text{workhours}} \) is the number of work hours per day multiplied by 6 days a week during a month.
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( \text{sell}_{k, i} \) be the quantity of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k, i} \) be the quantity of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k, i} \) be the quantity of product \( k \) stored at the end of month \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \cdot \text{sell}_{k, i} - \text{store\_price} \cdot \text{storage}_{k, i} \right)
\]

\subsection*{Constraints}
1. **Production Time Constraint**:
   \[
   \sum_{k=1}^{K} \sum_{m=1}^{M} \text{time}_{k, m} \cdot \text{manufacture}_{k, i} \leq n_{\text{workhours}} \cdot \left( \text{num}_m - \sum_{m=1}^{M} \text{maintain}_{i, m} \right) \quad \forall i
   \]

2. **Marketing Limitation**:
   \[
   \text{sell}_{k, i} \leq \text{limit}_{k, i} \quad \forall k, \forall i
   \]

3. **Storage Constraints**:
   \[
   \text{storage}_{k, i} = \text{storage}_{k, i-1} + \text{manufacture}_{k, i} - \text{sell}_{k, i} \quad \forall k, \forall i \; (i > 1)
   \]
   \[
   \text{storage}_{k, 1} = 0 \quad \forall k
   \]

4. **Ending Inventory Requirement**:
   \[
   \text{storage}_{k, I} \geq \text{keep\_quantity} \quad \forall k
   \]

5. **Non-negativity Constraints**:
   \[
   \text{sell}_{k, i} \geq 0, \quad \text{manufacture}_{k, i} \geq 0, \quad \text{storage}_{k, i} \geq 0 \quad \forall k, i
   \]

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], 
                 [0, 0, 0, 1, 1, 0], 
                 [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 1]],
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

#### Extracting data from the JSON-like data structure
num_m = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])  #### assuming limit has data for each month

profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I))

#### Constraints
#### Production Time Constraint
for i in range(I):
    constraint_expr = pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) for m in range(num_m))
    available_time = n_workhours * (sum(data['num_machines']) - sum(maintain[i][m] for m in range(num_m)))
    problem += constraint_expr <= available_time

#### Marketing Limitation
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i]

#### Storage Constraints
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i]
    #### Initial storage for month 1
    problem += storage[k][0] == 0

#### Ending Inventory Requirement
for k in range(K):
    problem += storage[k][I - 1] >= keep_quantity

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

