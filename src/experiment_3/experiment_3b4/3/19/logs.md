# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- A food is manufactured by refining raw oils and blending them together. 
- The raw oils are either vegetable oils or non-vegetable oils. 
- Each oil \var{i} may be purchased in month \var{m} for price \var{price_{i,m}}.
- The final product sells at \var{sell_price} per ton.
- Vegetable oils and non-vegetable oils require different production lines for refining. 
- In any month, it is not possible to refine more than \var{max_vegetable_refining_per_month} tons of vegetable oils and more than \var{max_non_vegetable_refining_per_month} tons of non-vegetable oils. 
- There is no loss of weight in the refining process, and the cost of refining may be ignored.
- It is possible to store up to \var{storage_size} tons of each raw oil for use later. 
- The cost of storage for both vegetable and non-vegetable oil is \var{storage_cost} per ton per month.
- The final product cannot be stored, nor can refined oils be stored.
- There is a technological restriction of hardness on the final product. 
- In the units in which hardness is measured, this must lie between \var{max_hardness} and \var{min_hardness}.
- The hardness product is computed by the weighted average of hardness of each oil.
- The hardness of oil \var{i} is \var{hardness_{i}}.
- At present, there are \var{init_amount} tons of each type of raw oil in storage. 
- We can assume that there is a month "0" to model the inital amount.
- It is required that at the end of the last month, we still have the same amout of storage as \var{init_amount}.
- This means directly adding the constraint that the storage in the last month must be equal to \var{init_amount}.
- The food may never be made up of more than three oils in any month.
- If an oil is used in a month, at least \var{min_usage} tons must be used.
- There are dependencies in the oil usage and \var{dependency_{i, j}} shows this relation
- If \var{dependency_{i, j}} is 1, then when oil \var{i} is used, oil \var{j} must also be used


INPUT FORMAT:

{
    "buy_price":[[price_{i, m} for i in 1,...,I] for m in 1,...,M],
    "sell_price": sell_price,
    "is_vegetable": [is_vegetable_{i} for i in 1,...,I],
    "max_vegetable_refining_per_month": max_veg,
    "max_non_vegetable_refining_per_month": max_non_veg,
    "storage_size": storage_size,
    "storage_cost": storage_cost,
    "max_hardness": max_hardness,
    "min_hardness": min_hardness,
    "hardness": [hardness_{i} for i in 1,...,I],
    "init_amount": init_amount,
    "min_usage": min_usage,
    "dependencies": [dependency_{i} for i in 1,...,I]
}


OBJECTIVE: What buying, storing and manufacturing policy should the company pursue in order to maximize profit?

OUTPUT INFO: 

- \var{buyquantity} represents the amount of buying quantity of each oil in each month
- \var{refine} represents the amount of refined quantity of each oil in each month
- \var{storage} represents the storage of each oil in each month
 
OUTPUT FORMAT: 

{
    "buy": [[buyquantity_{i, m} for i in 1,...,I] for m in 1,...M],
    "refine": [[refine_{i, m} for i in 1,...,I] for m in 1,...M],
    "storage": [[storage_{i, m} for i in 1,...,I] for m in 1,...,M]
} 
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( I \): Set of oils, indexed by \( i \).
    \item \( M \): Set of months, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{buy\_price}_{i,m} \): Purchase price of oil \( i \) in month \( m \).
    \item \( \text{sell\_price} \): Selling price of the final product per ton.
    \item \( \text{is\_vegetable}_i \): Indicator if oil \( i \) is vegetable (1 if true, 0 otherwise).
    \item \( \text{max\_vegetable\_refining\_per\_month} \): Maximum tons of vegetable oils that can be refined per month.
    \item \( \text{max\_non\_vegetable\_refining\_per\_month} \): Maximum tons of non-vegetable oils that can be refined per month.
    \item \( \text{storage\_size} \): Maximum storage capacity for each oil in tons.
    \item \( \text{storage\_cost} \): Storage cost per ton per month.
    \item \( \text{max\_hardness} \) and \( \text{min\_hardness} \): Bounds for the hardness of the final product.
    \item \( \text{hardness}_i \): Hardness of oil \( i \).
    \item \( \text{init\_amount} \): Initial storage of each oil in month 0.
    \item \( \text{min\_usage} \): Minimum usage of an oil if used in a month.
    \item \( \text{dependency}_{i,j} \): Dependency matrix, where 1 indicates oil \( j \) must be used if oil \( i \) is used.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{buyquantity}_{i,m} \): Tons of oil \( i \) purchased in month \( m \).
    \item \( \text{refine}_{i,m} \): Tons of oil \( i \) refined in month \( m \).
    \item \( \text{storage}_{i,m} \): Tons of oil \( i \) stored at the end of month \( m \).
    \item \( \text{use}_{i,m} \): Binary variable indicating whether oil \( i \) is used in month \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize profit over all months:
\[
\max \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buy\_price}_{i,m} \cdot \text{buyquantity}_{i,m} - \text{storage\_cost} \cdot \sum_{i=1}^{I} \text{storage}_{i,m} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Flow Balance:}
    \[
    \text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, \forall m
    \]
    \item \textbf{Refining Capacity:}
    \[
    \sum_{i \in \text{Vegetable}} \text{refine}_{i,m} \leq \text{max\_vegetable\_refining\_per\_month}, \quad \forall m
    \]
    \[
    \sum_{i \in \text{Non-Vegetable}} \text{refine}_{i,m} \leq \text{max\_non\_vegetable\_refining\_per\_month}, \quad \forall m
    \]
    \item \textbf{Storage Limit:}
    \[
    0 \leq \text{storage}_{i,m} \leq \text{storage\_size}, \quad \forall i, \forall m
    \]
    \item \textbf{Hardness Constraints:}
    \[
    \text{min\_hardness} \leq \frac{\sum_{i=1}^{I} \text{hardness}_i \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \leq \text{max\_hardness}, \quad \forall m
    \]
    \item \textbf{Initial and End Storage:}
    \[
    \text{storage}_{i,0} = \text{init\_amount}, \quad \text{storage}_{i,M} = \text{init\_amount}, \quad \forall i
    \]
    \item \textbf{Usage Constraints:}
    \[
    \text{refine}_{i,m} \geq \text{min\_usage} \cdot \text{use}_{i,m}, \quad \forall i, \forall m
    \]
    \[
    \sum_{i=1}^{I} \text{use}_{i,m} \leq 3, \quad \forall m
    \]
    \item \textbf{Dependency Constraints:}
    \[
    \text{use}_{i,m} \leq \text{use}_{j,m} + (1 - \text{dependency}_{i,j}), \quad \forall i, j, \forall m
    \]
    \item \textbf{Binary Constraints:}
    \[
    \text{use}_{i,m} \in \{0, 1\}, \quad \forall i, \forall m
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

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( I \): Set of oils, indexed by \( i \).
    \item \( M \): Set of months, indexed by \( m \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{buy\_price}_{i,m} \): Purchase price of oil \( i \) in month \( m \).
    \item \( \text{sell\_price} \): Selling price of the final product per ton.
    \item \( \text{is\_vegetable}_i \): Indicator if oil \( i \) is vegetable (1 if true, 0 otherwise).
    \item \( \text{max\_vegetable\_refining\_per\_month} \): Maximum tons of vegetable oils that can be refined per month.
    \item \( \text{max\_non\_vegetable\_refining\_per\_month} \): Maximum tons of non-vegetable oils that can be refined per month.
    \item \( \text{storage\_size} \): Maximum storage capacity for each oil in tons.
    \item \( \text{storage\_cost} \): Storage cost per ton per month.
    \item \( \text{max\_hardness} \) and \( \text{min\_hardness} \): Bounds for the hardness of the final product.
    \item \( \text{hardness}_i \): Hardness of oil \( i \).
    \item \( \text{init\_amount} \): Initial storage of each oil in month 0.
    \item \( \text{min\_usage} \): Minimum usage of an oil if used in a month.
    \item \( \text{dependency}_{i,j} \): Dependency matrix, where 1 indicates oil \( j \) must be used if oil \( i \) is used.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{buyquantity}_{i,m} \): Tons of oil \( i \) purchased in month \( m \).
    \item \( \text{refine}_{i,m} \): Tons of oil \( i \) refined in month \( m \).
    \item \( \text{storage}_{i,m} \): Tons of oil \( i \) stored at the end of month \( m \).
    \item \( \text{use}_{i,m} \): Binary variable indicating whether oil \( i \) is used in month \( m \).
\end{itemize}

\subsection*{Objective Function}
Maximize profit over all months:
\[
\max \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buy\_price}_{i,m} \cdot \text{buyquantity}_{i,m} - \text{storage\_cost} \cdot \sum_{i=1}^{I} \text{storage}_{i,m} \right)
\]

\subsection*{Constraints}
\begin{itemize}
    \item \textbf{Flow Balance:}
    \[
    \text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, \forall m
    \]
    \item \textbf{Refining Capacity:}
    \[
    \sum_{i \in \text{Vegetable}} \text{refine}_{i,m} \leq \text{max\_vegetable\_refining\_per\_month}, \quad \forall m
    \]
    \[
    \sum_{i \in \text{Non-Vegetable}} \text{refine}_{i,m} \leq \text{max\_non\_vegetable\_refining\_per\_month}, \quad \forall m
    \]
    \item \textbf{Storage Limit:}
    \[
    0 \leq \text{storage}_{i,m} \leq \text{storage\_size}, \quad \forall i, \forall m
    \]
    \item \textbf{Hardness Constraints:}
    \[
    \text{min\_hardness} \leq \frac{\sum_{i=1}^{I} \text{hardness}_i \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \leq \text{max\_hardness}, \quad \forall m
    \]
    \item \textbf{Initial and End Storage:}
    \[
    \text{storage}_{i,0} = \text{init\_amount}, \quad \text{storage}_{i,M} = \text{init\_amount}, \quad \forall i
    \]
    \item \textbf{Usage Constraints:}
    \[
    \text{refine}_{i,m} \geq \text{min\_usage} \cdot \text{use}_{i,m}, \quad \forall i, \forall m
    \]
    \[
    \sum_{i=1}^{I} \text{use}_{i,m} \leq 3, \quad \forall m
    \]
    \item \textbf{Dependency Constraints:}
    \[
    \text{use}_{i,m} \leq \text{use}_{j,m} + (1 - \text{dependency}_{i,j}), \quad \forall i, j, \forall m
    \]
    \item \textbf{Binary Constraints:}
    \[
    \text{use}_{i,m} \in \{0, 1\}, \quad \forall i, \forall m
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'])  #### Number of oils
M = len(data['buy_price'][0])  #### Number of months

#### Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

#### Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

#### Objective
revenue = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M))
costs = pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i, m] for i in range(I) for m in range(M))
storage_costs = pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))
problem += revenue - costs - storage_costs

#### Constraints
for m in range(M):
    #### Flow balance
    for i in range(I):
        if m == 0:
            problem += storage[i, m] == data['init_amount'] + buy_quantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy_quantity[i, m] - refine[i, m]

    #### Refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    #### Hardness constraints
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    if total_refine > 0:
        hardness_expr = pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
        problem += hardness_expr >= data['min_hardness'] * total_refine
        problem += hardness_expr <= data['max_hardness'] * total_refine

    #### Usage constraints
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

    #### Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j]:
                problem += use[i, m] <= use[j, m] + 1 - data['dependencies'][i][j]

#### Storage limits
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

#### Initial and end storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

#### Solve
problem.solve()

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

#### Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'])  #### Number of oils
M = len(data['buy_price'][0])  #### Number of months

#### Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

#### Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

#### Objective
revenue = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M))
costs = pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i, m] for i in range(I) for m in range(M))
storage_costs = pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))
problem += revenue - costs - storage_costs

#### Constraints
for m in range(M):
    #### Flow balance
    for i in range(I):
        if m == 0:
            problem += storage[i, m] == data['init_amount'] + buy_quantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy_quantity[i, m] - refine[i, m]

    #### Refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    #### Hardness constraints
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    if total_refine > 0:
        hardness_expr = pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
        problem += hardness_expr >= data['min_hardness'] * total_refine
        problem += hardness_expr <= data['max_hardness'] * total_refine

    #### Usage constraints
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

    #### Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j]:
                problem += use[i, m] <= use[j, m] + 1 - data['dependencies'][i][j]

#### Storage limits
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

#### Initial and end storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

#### Solve
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/3/19/python_code0.py", line 48, in <module>
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b4/3/19/python_code0.py", line 48, in <genexpr>
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
                                                            ~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'])  #### Number of oils
M = len(data['buy_price'][0])  #### Number of months

#### Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

#### Problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

#### Objective
revenue = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M))
costs = pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i, m] for i in range(I) for m in range(M))
storage_costs = pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))
problem += revenue - costs - storage_costs

#### Constraints
for m in range(M):
    #### Flow balance
    for i in range(I):
        if m == 0:
            problem += storage[i, m] == data['init_amount'] + buy_quantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buy_quantity[i, m] - refine[i, m]

    #### Refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    #### Hardness constraints
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += total_refine >= 0  #### Ensure total_refine is non-negative first
    hardness_expr = pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
    problem += hardness_expr >= data['min_hardness'] * total_refine
    problem += hardness_expr <= data['max_hardness'] * total_refine

    #### Usage constraints
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

    #### Dependency constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j]:
                problem += use[i, m] <= use[j, m] + 1 - data['dependencies'][i][j]

#### Storage limits
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

#### Initial and end storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

#### Solve
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

