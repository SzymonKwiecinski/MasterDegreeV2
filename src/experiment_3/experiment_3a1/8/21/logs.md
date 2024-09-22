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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the total number of machines.
    \item Let \( K \) be the total number of products.
    \item Let \( I \) be the total number of months.
    \item \( \text{profit}_k \): profit from product \( k \).
    \item \( \text{time}_{k,m} \): time required to produce product \( k \) on machine \( m \).
    \item \( \text{down}_m \): downtime for maintenance for machine \( m \).
    \item \( \text{limit}_{k,i} \): marketing limitation for product \( k \) in month \( i \).
    \item \( \text{store\_price} \): storage cost per unit per month.
    \item \( \text{keep\_quantity} \): desired stock of each product at the end of the subsequent months.
    \item \( \text{n\_workhours} \): total working hours available in a month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{sell}_{k,i} \): amount of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k,i} \): amount of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k,i} \): amount of product \( k \) stored at the end of month \( i \).
    \item \( \text{maintain}_{m,i} \): number of machines under maintenance in month \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Maximize} \quad Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \text{profit}_k \cdot \text{sell}_{k,i} - \sum_{i=1}^{I} \sum_{k=1}^{K} \text{store\_price} \cdot \text{storage}_{k,i}
\]

\subsection*{Constraints}

\begin{enumerate}
    \item \textbf{Production Constraint:}
    \[
    \sum_{k=1}^{K} \text{time}_{k,m} \cdot \text{manufacture}_{k,i} \leq n \cdot \text{n\_workhours} \quad \forall m, i
    \]

    \item \textbf{Sales Limitations:}
    \[
    \text{sell}_{k,i} \leq \text{limit}_{k,i} \quad \forall k, i
    \]

    \item \textbf{Storage Balance:}
    \[
    \text{storage}_{k,i} = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i} \quad \forall k, i
    \]
    with \( \text{storage}_{k,0} = 0 \).

    \item \textbf{End of Month Stock Requirement:}
    \[
    \text{storage}_{k,I} \geq \text{keep\_quantity} \quad \forall k
    \]

    \item \textbf{Maintenance Constraint:}
    \[
    \sum_{m=1}^{M} \text{maintain}_{m,i} \leq \text{down}_{m} \quad \forall i
    \]

    \item \textbf{Non-negativity and Integer Constraints:}
    \[
    \text{sell}_{k,i}, \text{manufacture}_{k,i}, \text{storage}_{k,i} \geq 0 \quad \forall k, i
    \]
    \[
    \text{maintain}_{m,i} \in \mathbb{Z}^{+} \quad \forall m, i
    \]
\end{enumerate}

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

\subsection*{Parameters}
\begin{itemize}
    \item Let \( M \) be the total number of machines.
    \item Let \( K \) be the total number of products.
    \item Let \( I \) be the total number of months.
    \item \( \text{profit}_k \): profit from product \( k \).
    \item \( \text{time}_{k,m} \): time required to produce product \( k \) on machine \( m \).
    \item \( \text{down}_m \): downtime for maintenance for machine \( m \).
    \item \( \text{limit}_{k,i} \): marketing limitation for product \( k \) in month \( i \).
    \item \( \text{store\_price} \): storage cost per unit per month.
    \item \( \text{keep\_quantity} \): desired stock of each product at the end of the subsequent months.
    \item \( \text{n\_workhours} \): total working hours available in a month.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{sell}_{k,i} \): amount of product \( k \) sold in month \( i \).
    \item \( \text{manufacture}_{k,i} \): amount of product \( k \) manufactured in month \( i \).
    \item \( \text{storage}_{k,i} \): amount of product \( k \) stored at the end of month \( i \).
    \item \( \text{maintain}_{m,i} \): number of machines under maintenance in month \( i \).
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:

\[
\text{Maximize} \quad Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \text{profit}_k \cdot \text{sell}_{k,i} - \sum_{i=1}^{I} \sum_{k=1}^{K} \text{store\_price} \cdot \text{storage}_{k,i}
\]

\subsection*{Constraints}

\begin{enumerate}
    \item \textbf{Production Constraint:}
    \[
    \sum_{k=1}^{K} \text{time}_{k,m} \cdot \text{manufacture}_{k,i} \leq n \cdot \text{n\_workhours} \quad \forall m, i
    \]

    \item \textbf{Sales Limitations:}
    \[
    \text{sell}_{k,i} \leq \text{limit}_{k,i} \quad \forall k, i
    \]

    \item \textbf{Storage Balance:}
    \[
    \text{storage}_{k,i} = \text{storage}_{k,i-1} + \text{manufacture}_{k,i} - \text{sell}_{k,i} \quad \forall k, i
    \]
    with \( \text{storage}_{k,0} = 0 \).

    \item \textbf{End of Month Stock Requirement:}
    \[
    \text{storage}_{k,I} \geq \text{keep\_quantity} \quad \forall k
    \]

    \item \textbf{Maintenance Constraint:}
    \[
    \sum_{m=1}^{M} \text{maintain}_{m,i} \leq \text{down}_{m} \quad \forall i
    \]

    \item \textbf{Non-negativity and Integer Constraints:}
    \[
    \text{sell}_{k,i}, \text{manufacture}_{k,i}, \text{storage}_{k,i} \geq 0 \quad \forall k, i
    \]
    \[
    \text{maintain}_{m,i} \in \mathbb{Z}^{+} \quad \forall m, i
    \]
\end{enumerate}

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

#### Model Setup
problem = pulp.LpProblem("MixedIntegerLinearProgramming", pulp.LpMaximize)

#### Parameters
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
time = data['time']
limit = data['limit']
down = data['down'][0]

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[(k, i)] for k in range(K) for i in range(I)) - \
           pulp.lpSum(store_price * storage[(k, i)] for k in range(K) for i in range(I))

#### Production Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(K)) <= data['num_machines'][m] * n_workhours

#### Sales Limitations
for k in range(K):
    for i in range(I):
        problem += sell[(k, i)] <= limit[k][i]

#### Storage Balance
for k in range(K):
    for i in range(1, I):
        problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)]

#### Initial Condition for Storage
for k in range(K):
    problem += storage[(k, 0)] == 0

#### End of Month Stock Requirement
for k in range(K):
    problem += storage[(k, I-1)] >= keep_quantity

#### Maintenance Constraint
for i in range(I):
    problem += pulp.lpSum(maintain[(m, i)] for m in range(M)) <= sum(down)

#### Solve the Problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

