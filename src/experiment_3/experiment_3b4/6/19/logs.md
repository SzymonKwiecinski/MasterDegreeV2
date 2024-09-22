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
To model this problem using linear programming, here is the mathematical formulation in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Indices:}
\begin{align*}
i & : \text{ index for oils, } i = 1, \ldots, I \\
m & : \text{ index for months, } m = 1, \ldots, M 
\end{align*}

\textbf{Parameters:}
\begin{align*}
\text{buy\_price}_{i,m} & : \text{ Buying price of oil } i \text{ in month } m \\
\text{sell\_price} & : \text{ Selling price of the final product per ton} \\
\text{is\_vegetable}_i & : \begin{cases} 
1, & \text{if oil } i \text{ is a vegetable oil} \\ 
0, & \text{otherwise} 
\end{cases} \\
\text{max\_veg} & : \text{ Maximum refining capacity for vegetable oils per month} \\
\text{max\_non\_veg} & : \text{ Maximum refining capacity for non-vegetable oils per month} \\
\text{storage\_size} & : \text{ Maximum storage capacity for each raw oil} \\
\text{storage\_cost} & : \text{ Cost of storing raw oil per ton per month} \\
\text{max\_hardness} & : \text{ Maximum allowable hardness of the final product} \\
\text{min\_hardness} & : \text{ Minimum allowable hardness of the final product} \\
\text{hardness}_i & : \text{ Hardness of oil } i \\
\text{init\_amount} & : \text{ Initial amount of each type of raw oil in storage} \\
\text{min\_usage} & : \text{ Minimum usage of each oil if used in a month} \\
\text{dependencies}_{i,j} & : \begin{cases} 
1, & \text{if oil } i \text{ requires the use of oil } j \\ 
0, & \text{otherwise} 
\end{cases} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{buyquantity}_{i,m} & : \text{ Quantity of oil } i \text{ purchased in month } m \\
\text{refine}_{i,m} & : \text{ Quantity of oil } i \text{ refined in month } m \\
\text{storage}_{i,m} & : \text{ Quantity of oil } i \text{ stored at the end of month } m \\
\text{use}_{i,m} & : \begin{cases} 
1, & \text{if oil } i \text{ is used in month } m \\ 
0, & \text{otherwise} 
\end{cases}
\end{align*}

\textbf{Objective: Maximize Profit}
\[
\max \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buy\_price}_{i,m} \cdot \text{buyquantity}_{i,m} - \text{storage\_cost} \cdot \sum_{i=1}^{I} \text{storage}_{i,m} \right)
\]

\textbf{Constraints:}
\begin{align*}
& \text{Storage balance for each oil and month:} \\
& \text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, m \\
& \text{Initial storage:} \\
& \text{storage}_{i,0} = \text{init\_amount}, \quad \forall i \\
& \text{Final storage requirement:} \\
& \text{storage}_{i,M} = \text{init\_amount}, \quad \forall i \\
& \text{Storage capacity limit:} \\
& 0 \leq \text{storage}_{i,m} \leq \text{storage\_size}, \quad \forall i, m \\
& \text{Vegetable oil refining capacity:} \\
& \sum_{i: \text{is\_vegetable}_i = 1} \text{refine}_{i,m} \leq \text{max\_veg}, \quad \forall m \\
& \text{Non-vegetable oil refining capacity:} \\
& \sum_{i: \text{is\_vegetable}_i = 0} \text{refine}_{i,m} \leq \text{max\_non\_veg}, \quad \forall m \\
& \text{Hardness requirement:} \\
& \min\_hardness \leq \frac{\sum_{i=1}^{I} \text{hardness}_i \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \leq \max\_hardness, \quad \forall m \\
& \text{Usage restrictions:} \\
& \sum_{i=1}^{I} \text{use}_{i,m} \leq 3, \quad \forall m \\
& \text{Minimum usage if used:} \\
& \text{refine}_{i,m} \geq \text{min\_usage} \cdot \text{use}_{i,m}, \quad \forall i, m \\
& \text{Dependency constraints:} \\
& \text{use}_{i,m} \geq \text{dependencies}_{i,j} \cdot \text{use}_{j,m}, \quad \forall i, j, m \\
& \text{Non-negativity:} \\
& \text{buyquantity}_{i,m}, \text{refine}_{i,m}, \text{storage}_{i,m} \geq 0, \quad \forall i, m \\
& \text{Binary:} \\
& \text{use}_{i,m} \in \{0,1\}, \quad \forall i, m 
\end{align*}

\end{document}
```

This model captures the buying, refining, and storing decisions subject to the constraints outlined in the problem description, aiming to maximize the profit over the given planning horizon of months. The objective function and constraints are structured to reflect the real-world operational limitations and conditions specified.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Indices:}
\begin{align*}
i & : \text{ index for oils, } i = 1, \ldots, I \\
m & : \text{ index for months, } m = 1, \ldots, M 
\end{align*}

\textbf{Parameters:}
\begin{align*}
\text{buy\_price}_{i,m} & : \text{ Buying price of oil } i \text{ in month } m \\
\text{sell\_price} & : \text{ Selling price of the final product per ton} \\
\text{is\_vegetable}_i & : \begin{cases} 
1, & \text{if oil } i \text{ is a vegetable oil} \\ 
0, & \text{otherwise} 
\end{cases} \\
\text{max\_veg} & : \text{ Maximum refining capacity for vegetable oils per month} \\
\text{max\_non\_veg} & : \text{ Maximum refining capacity for non-vegetable oils per month} \\
\text{storage\_size} & : \text{ Maximum storage capacity for each raw oil} \\
\text{storage\_cost} & : \text{ Cost of storing raw oil per ton per month} \\
\text{max\_hardness} & : \text{ Maximum allowable hardness of the final product} \\
\text{min\_hardness} & : \text{ Minimum allowable hardness of the final product} \\
\text{hardness}_i & : \text{ Hardness of oil } i \\
\text{init\_amount} & : \text{ Initial amount of each type of raw oil in storage} \\
\text{min\_usage} & : \text{ Minimum usage of each oil if used in a month} \\
\text{dependencies}_{i,j} & : \begin{cases} 
1, & \text{if oil } i \text{ requires the use of oil } j \\ 
0, & \text{otherwise} 
\end{cases} \\
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{buyquantity}_{i,m} & : \text{ Quantity of oil } i \text{ purchased in month } m \\
\text{refine}_{i,m} & : \text{ Quantity of oil } i \text{ refined in month } m \\
\text{storage}_{i,m} & : \text{ Quantity of oil } i \text{ stored at the end of month } m \\
\text{use}_{i,m} & : \begin{cases} 
1, & \text{if oil } i \text{ is used in month } m \\ 
0, & \text{otherwise} 
\end{cases}
\end{align*}

\textbf{Objective: Maximize Profit}
\[
\max \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buy\_price}_{i,m} \cdot \text{buyquantity}_{i,m} - \text{storage\_cost} \cdot \sum_{i=1}^{I} \text{storage}_{i,m} \right)
\]

\textbf{Constraints:}
\begin{align*}
& \text{Storage balance for each oil and month:} \\
& \text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, m \\
& \text{Initial storage:} \\
& \text{storage}_{i,0} = \text{init\_amount}, \quad \forall i \\
& \text{Final storage requirement:} \\
& \text{storage}_{i,M} = \text{init\_amount}, \quad \forall i \\
& \text{Storage capacity limit:} \\
& 0 \leq \text{storage}_{i,m} \leq \text{storage\_size}, \quad \forall i, m \\
& \text{Vegetable oil refining capacity:} \\
& \sum_{i: \text{is\_vegetable}_i = 1} \text{refine}_{i,m} \leq \text{max\_veg}, \quad \forall m \\
& \text{Non-vegetable oil refining capacity:} \\
& \sum_{i: \text{is\_vegetable}_i = 0} \text{refine}_{i,m} \leq \text{max\_non\_veg}, \quad \forall m \\
& \text{Hardness requirement:} \\
& \min\_hardness \leq \frac{\sum_{i=1}^{I} \text{hardness}_i \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \leq \max\_hardness, \quad \forall m \\
& \text{Usage restrictions:} \\
& \sum_{i=1}^{I} \text{use}_{i,m} \leq 3, \quad \forall m \\
& \text{Minimum usage if used:} \\
& \text{refine}_{i,m} \geq \text{min\_usage} \cdot \text{use}_{i,m}, \quad \forall i, m \\
& \text{Dependency constraints:} \\
& \text{use}_{i,m} \geq \text{dependencies}_{i,j} \cdot \text{use}_{j,m}, \quad \forall i, j, m \\
& \text{Non-negativity:} \\
& \text{buyquantity}_{i,m}, \text{refine}_{i,m}, \text{storage}_{i,m} \geq 0, \quad \forall i, m \\
& \text{Binary:} \\
& \text{use}_{i,m} \in \{0,1\}, \quad \forall i, m 
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'buy_price': [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135]
    ],
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
    'dependencies': [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

#### Problem
problem = pulp.LpProblem("OilBlending", pulp.LpMaximize)

#### Sets
I = len(data['is_vegetable'])
M = len(data['buy_price'][0])

#### Decision Variables
buyquantity = pulp.LpVariable.dicts('buyquantity', ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
refine = pulp.LpVariable.dicts('refine', ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
storage = pulp.LpVariable.dicts('storage', ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat=pulp.LpContinuous)
use = pulp.LpVariable.dicts('use', ((i, m) for i in range(I) for m in range(M)), cat=pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum([
    data['sell_price'] * refine[i, m] - data['buy_price'][i][m] * buyquantity[i, m] - data['storage_cost'] * storage[i, m]
    for i in range(I) for m in range(M)
])

#### Constraints
#### Initial storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

#### Storage balance
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1]

#### Final storage requirement
for i in range(I):
    problem += storage[i, M] == data['init_amount']

#### Storage capacity limit
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] <= data['storage_size']

#### Vegetable oil refining capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']

#### Non-vegetable oil refining capacity
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

#### Hardness requirement
for m in range(M):
    refine_sum = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * refine_sum
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * refine_sum

#### Usage restrictions
for m in range(M):
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

#### Minimum usage if used
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

#### Dependency constraints
for i in range(I):
    for j in range(I):
        for m in range(M):
            if data['dependencies'][i][j]:
                problem += use[i, m] >= use[j, m]

#### Solve
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

