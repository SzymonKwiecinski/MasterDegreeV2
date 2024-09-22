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

\section*{Linear Programming Model for Factory Production and Profit Maximization}

\subsection*{Parameters}

\begin{align*}
& num_m \text{ : Number of machines} \\
& profit_k \text{ : Profit from product } k \\
& time_{k,m} \text{ : Production time for product } k \text{ on machine } m \\
& maintain_{i,m} \text{ : Number of machines down in month } i \\
& limit_{k,i} \text{ : Marketing limitation for product } k \text{ in month } i \\
& store\_price \text{ : Cost of storing per unit per month} \\
& keep\_quantity \text{ : Required quantity to keep in storage} \\
& n\_workhours \text{ : Number of work hours in a day} \\
& I \text{ : Total months} \\
& K \text{ : Total products}
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
& sell_{k,i} \text{ : Amount of product } k \text{ sold in month } i \\
& manufacture_{k,i} \text{ : Amount of product } k \text{ manufactured in month } i \\
& storage_{k,i} \text{ : Amount of product } k \text{ stored at the end of month } i
\end{align*}

\subsection*{Objective Function}

Maximize the total profit:
\[
Z = \sum_{i=1}^{I} \sum_{k=1}^{K} (profit_k \cdot sell_{k,i} - store\_price \cdot storage_{k,i})
\]

\subsection*{Constraints}

1. \textbf{Production Time Constraint:}
\[
\sum_{k=1}^{K} \sum_{m=1}^{num_m} time_{k,m} \cdot manufacture_{k,i} \leq (n\_workhours \cdot 6 \cdot 24) - \sum_{m=1}^{num_m} maintain_{i,m} \text{ for all } i
\]

2. \textbf{Marketing Limitation:}
\[
sell_{k,i} \leq limit_{k,i} \text{ for all } k \text{ and } i
\]

3. \textbf{Storage Limits:}
\[
storage_{k,i} \leq 100 \text{ for all } k \text{ and } i
\]

4. \textbf{Storage Balance:}
\[
storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} = storage_{k,i} \text{ for all } k \text{ and } i > 1
\]

5. \textbf{Initial Storage Condition:}
\[
storage_{k,1} = 0 \text{ for all } k
\]

6. \textbf{End Storage Requirement:}
\[
storage_{k,I} \geq keep\_quantity \text{ for all } k
\]

7. \textbf{Non-negativity Constraints:}
\[
sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0 \text{ for all } k, i
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

\section*{Linear Programming Model for Factory Production and Profit Maximization}

\subsection*{Parameters}

\begin{align*}
& num_m \text{ : Number of machines} \\
& profit_k \text{ : Profit from product } k \\
& time_{k,m} \text{ : Production time for product } k \text{ on machine } m \\
& maintain_{i,m} \text{ : Number of machines down in month } i \\
& limit_{k,i} \text{ : Marketing limitation for product } k \text{ in month } i \\
& store\_price \text{ : Cost of storing per unit per month} \\
& keep\_quantity \text{ : Required quantity to keep in storage} \\
& n\_workhours \text{ : Number of work hours in a day} \\
& I \text{ : Total months} \\
& K \text{ : Total products}
\end{align*}

\subsection*{Decision Variables}

\begin{align*}
& sell_{k,i} \text{ : Amount of product } k \text{ sold in month } i \\
& manufacture_{k,i} \text{ : Amount of product } k \text{ manufactured in month } i \\
& storage_{k,i} \text{ : Amount of product } k \text{ stored at the end of month } i
\end{align*}

\subsection*{Objective Function}

Maximize the total profit:
\[
Z = \sum_{i=1}^{I} \sum_{k=1}^{K} (profit_k \cdot sell_{k,i} - store\_price \cdot storage_{k,i})
\]

\subsection*{Constraints}

1. \textbf{Production Time Constraint:}
\[
\sum_{k=1}^{K} \sum_{m=1}^{num_m} time_{k,m} \cdot manufacture_{k,i} \leq (n\_workhours \cdot 6 \cdot 24) - \sum_{m=1}^{num_m} maintain_{i,m} \text{ for all } i
\]

2. \textbf{Marketing Limitation:}
\[
sell_{k,i} \leq limit_{k,i} \text{ for all } k \text{ and } i
\]

3. \textbf{Storage Limits:}
\[
storage_{k,i} \leq 100 \text{ for all } k \text{ and } i
\]

4. \textbf{Storage Balance:}
\[
storage_{k,i-1} + manufacture_{k,i} - sell_{k,i} = storage_{k,i} \text{ for all } k \text{ and } i > 1
\]

5. \textbf{Initial Storage Condition:}
\[
storage_{k,1} = 0 \text{ for all } k
\]

6. \textbf{End Storage Requirement:}
\[
storage_{k,I} \geq keep\_quantity \text{ for all } k
\]

7. \textbf{Non-negativity Constraints:}
\[
sell_{k,i} \geq 0, \quad manufacture_{k,i} \geq 0, \quad storage_{k,i} \geq 0 \text{ for all } k, i
\]

\end{document}</MATH_MODEL>
<DATA>
{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data initialization
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0],
                 [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500],
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300],
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500],
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

num_machines = len(data['num_machines'])
I = len(data['maintain'])
K = len(data['profit'])
n_workhours = data['n_workhours']
store_price = data['store_price']
keep_quantity = data['keep_quantity']

#### Create the problem
problem = pulp.LpProblem("Factory_Production_Profit_Maximization", pulp.LpMaximize)

#### Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(1, I + 1))

#### Constraints
#### Production Time Constraint
for i in range(1, I + 1):
    total_time = pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K) for m in range(num_machines))
    maintain_down = sum(data['maintain'][i-1][m] for m in range(num_machines))
    problem += total_time <= (n_workhours * 6 * 24) - maintain_down

#### Marketing Limitation
for k in range(K):
    for i in range(1, I + 1):
        problem += sell[k, i] <= data['limit'][i-1][k]

#### Storage Limits
for k in range(K):
    for i in range(1, I + 1):
        problem += storage[k, i] <= 100

#### Storage Balance
for k in range(K):
    for i in range(2, I + 1):
        problem += storage[k, i - 1] + manufacture[k, i] - sell[k, i] == storage[k, i]

#### Initial Storage Condition
for k in range(K):
    problem += storage[k, 1] == 0

#### End Storage Requirement
for k in range(K):
    problem += storage[k, I] >= keep_quantity

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

