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

\section*{MILP Model for Engineering Factory Operations}

\textbf{Parameters:}
\begin{itemize}
    \item Let \( M \) be the number of machines.
    \item Let \( K \) be the number of products.
    \item Let \( I \) be the number of months.
    \item \( \text{profit}_k \): Profit per unit of product \( k \).
    \item \( \text{time}_{k,m} \): Production time required for product \( k \) on machine \( m \).
    \item \( \text{down}_m \): Number of months machine \( m \) is under maintenance.
    \item \( \text{limit}_{k,i} \): Sales limit for product \( k \) in month \( i \).
    \item \( \text{store\_price} \): Storage cost per unit per month.
    \item \( \text{keep\_quantity} \): Desired stock of each product at the end of the planning period.
    \item \( n_{\text{workhours}} \): Number of work hours available per day.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{sell}_{k,i} \): Quantity of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k,i} \): Quantity of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k,i} \): Quantity of product \( k \) stored at the end of month \( i \).
    \item \( \text{maintain}_{m,i} \): Binary variable indicating whether machine \( m \) is under maintenance in month \( i \) (1 if under maintenance, 0 otherwise).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \cdot \text{sell}_{k,i} - \text{store\_price} \cdot \text{storage}_{k,i} \right)
\]

\textbf{Subject to:}

\begin{align*}
\sum_{k=1}^{K} \text{manufacture}_{k,i} \cdot \text{time}_{k,m} & \leq n_{\text{workhours}} \cdot 12 \cdot (24 - \text{down}_m) \quad \forall m \in \{1, \ldots, M\}, i \in \{1, \ldots, I\} \\
\text{sell}_{k,i} & \leq \text{limit}_{k,i} \quad \forall k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
\text{storage}_{k,i} & = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i} \quad \forall k \in \{1, \ldots, K\}, i \in \{2, \ldots, I\} \\
\text{storage}_{k,1} & = 0 \quad \forall k \in \{1, \ldots, K\} \\
\text{storage}_{k,I} & \geq \text{keep\_quantity} \quad \forall k \in \{1, \ldots, K\} \\
\sum_{i=1}^{I} \text{maintain}_{m,i} & \leq \text{down}_m \quad \forall m \in \{1, \ldots, M\} \\
\text{manufacture}_{k,i}, \text{sell}_{k,i}, \text{storage}_{k,i} & \geq 0 \quad \forall k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
\text{maintain}_{m,i} & \in \{0, 1\} \quad \forall m \in \{1, \ldots, M\}, i \in \{1, \ldots, I\}
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

\section*{MILP Model for Engineering Factory Operations}

\textbf{Parameters:}
\begin{itemize}
    \item Let \( M \) be the number of machines.
    \item Let \( K \) be the number of products.
    \item Let \( I \) be the number of months.
    \item \( \text{profit}_k \): Profit per unit of product \( k \).
    \item \( \text{time}_{k,m} \): Production time required for product \( k \) on machine \( m \).
    \item \( \text{down}_m \): Number of months machine \( m \) is under maintenance.
    \item \( \text{limit}_{k,i} \): Sales limit for product \( k \) in month \( i \).
    \item \( \text{store\_price} \): Storage cost per unit per month.
    \item \( \text{keep\_quantity} \): Desired stock of each product at the end of the planning period.
    \item \( n_{\text{workhours}} \): Number of work hours available per day.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( \text{sell}_{k,i} \): Quantity of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k,i} \): Quantity of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k,i} \): Quantity of product \( k \) stored at the end of month \( i \).
    \item \( \text{maintain}_{m,i} \): Binary variable indicating whether machine \( m \) is under maintenance in month \( i \) (1 if under maintenance, 0 otherwise).
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{profit}_k \cdot \text{sell}_{k,i} - \text{store\_price} \cdot \text{storage}_{k,i} \right)
\]

\textbf{Subject to:}

\begin{align*}
\sum_{k=1}^{K} \text{manufacture}_{k,i} \cdot \text{time}_{k,m} & \leq n_{\text{workhours}} \cdot 12 \cdot (24 - \text{down}_m) \quad \forall m \in \{1, \ldots, M\}, i \in \{1, \ldots, I\} \\
\text{sell}_{k,i} & \leq \text{limit}_{k,i} \quad \forall k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
\text{storage}_{k,i} & = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i} \quad \forall k \in \{1, \ldots, K\}, i \in \{2, \ldots, I\} \\
\text{storage}_{k,1} & = 0 \quad \forall k \in \{1, \ldots, K\} \\
\text{storage}_{k,I} & \geq \text{keep\_quantity} \quad \forall k \in \{1, \ldots, K\} \\
\sum_{i=1}^{I} \text{maintain}_{m,i} & \leq \text{down}_m \quad \forall m \in \{1, \ldots, M\} \\
\text{manufacture}_{k,i}, \text{sell}_{k,i}, \text{storage}_{k,i} & \geq 0 \quad \forall k \in \{1, \ldots, K\}, i \in \{1, \ldots, I\} \\
\text{maintain}_{m,i} & \in \{0, 1\} \quad \forall m \in \{1, \ldots, M\}, i \in \{1, \ldots, I\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'down': [[0, 1, 1, 1, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

#### Extract data
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Create decision variables
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), cat='Binary')

#### Objective function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(num_products) for i in range(num_months))

#### Constraints
for m in range(num_machines):
    for i in range(num_months):
        problem += (pulp.lpSum(manufacture[k][i] * time[k][m] for k in range(num_products)) 
                     <= n_workhours * 12 * (24 - down[m]))

for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i]

for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

for k in range(num_products):
    problem += storage[k][0] == 0

for k in range(num_products):
    problem += storage[k][num_months - 1] >= keep_quantity

for m in range(num_machines):
    problem += pulp.lpSum(maintain[m][i] for i in range(num_months)) <= down[m]

for k in range(num_products):
    for i in range(num_months):
        problem += manufacture[k][i] >= 0
        problem += sell[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(num_machines):
    for i in range(num_months):
        maintain[m][i].cat = pulp.LpBinary

#### Solve the problem
problem.solve()

#### Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

