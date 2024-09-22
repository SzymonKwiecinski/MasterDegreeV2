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

\section*{Mathematical Model for Oil Blending Problem}

\subsection*{Indices}
\begin{itemize}
    \item $i$: index for oil types, where $i = 1, ..., I$
    \item $m$: index for months, where $m = 0, ..., M$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $price_{i,m}$: price of oil $i$ in month $m$
    \item $sell\_price$: selling price of the final product per ton
    \item $is\_vegetable_{i}$: binary indicator for whether oil $i$ is vegetable or non-vegetable
    \item $max\_veg$: maximum refining capacity for vegetable oils per month
    \item $max\_veg$: maximum refining capacity for non-vegetable oils per month
    \item $storage\_size$: maximum storage capacity for each oil
    \item $storage\_cost$: cost of storage per ton per month
    \item $max\_hardness$: upper limit on hardness of the final product
    \item $min\_hardness$: lower limit on hardness of the final product
    \item $hardness_{i}$: hardness of oil $i$
    \item $init\_amount$: initial amount of each oil at month 0
    \item $min\_usage$: minimum usage requirement for each oil used
    \item $dependency_{i,j}$: binary indicator for dependency between oils $i$ and $j$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}

\subsubsection*{Storage Dynamics}
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m \geq 1
\]
\[
storage_{i,0} = init\_amount, \quad \forall i
\]

\subsubsection*{Storage Capacity}
\[
storage_{i,m} \leq storage\_size, \quad \forall i, m
\]

\subsubsection*{Refining Capacity}
\[
\sum_{i \in \text{vegetable}} refine_{i,m} \leq max\_veg, \quad \forall m
\]
\[
\sum_{i \in \text{non-vegetable}} refine_{i,m} \leq max\_veg, \quad \forall m
\]

\subsubsection*{Final Product Hardness Condition}
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m
\]

\subsubsection*{Initial and Final Storage Constraint}
\[
storage_{i,M} = init\_amount, \quad \forall i
\]

\subsubsection*{Usage Requirements and Dependencies}
\[
refine_{i,m} \geq min\_usage \cdot (y_i), \quad \forall i, m
\]
\[
y_i \in \{0, 1\} \quad \text{(binary variable indicating if oil $i$ is used in month $m$)}
\]
\[
y_j \geq dependency_{i,j} \cdot y_i, \quad \forall i,j
\]

\subsubsection*{Limitation on Oils per Month}
\[
\sum_{i=1}^{I} y_i \leq 3, \quad \forall m
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

\section*{Mathematical Model for Oil Blending Problem}

\subsection*{Indices}
\begin{itemize}
    \item $i$: index for oil types, where $i = 1, ..., I$
    \item $m$: index for months, where $m = 0, ..., M$
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $price_{i,m}$: price of oil $i$ in month $m$
    \item $sell\_price$: selling price of the final product per ton
    \item $is\_vegetable_{i}$: binary indicator for whether oil $i$ is vegetable or non-vegetable
    \item $max\_veg$: maximum refining capacity for vegetable oils per month
    \item $max\_veg$: maximum refining capacity for non-vegetable oils per month
    \item $storage\_size$: maximum storage capacity for each oil
    \item $storage\_cost$: cost of storage per ton per month
    \item $max\_hardness$: upper limit on hardness of the final product
    \item $min\_hardness$: lower limit on hardness of the final product
    \item $hardness_{i}$: hardness of oil $i$
    \item $init\_amount$: initial amount of each oil at month 0
    \item $min\_usage$: minimum usage requirement for each oil used
    \item $dependency_{i,j}$: binary indicator for dependency between oils $i$ and $j$
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}

\subsubsection*{Storage Dynamics}
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m \geq 1
\]
\[
storage_{i,0} = init\_amount, \quad \forall i
\]

\subsubsection*{Storage Capacity}
\[
storage_{i,m} \leq storage\_size, \quad \forall i, m
\]

\subsubsection*{Refining Capacity}
\[
\sum_{i \in \text{vegetable}} refine_{i,m} \leq max\_veg, \quad \forall m
\]
\[
\sum_{i \in \text{non-vegetable}} refine_{i,m} \leq max\_veg, \quad \forall m
\]

\subsubsection*{Final Product Hardness Condition}
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m
\]

\subsubsection*{Initial and Final Storage Constraint}
\[
storage_{i,M} = init\_amount, \quad \forall i
\]

\subsubsection*{Usage Requirements and Dependencies}
\[
refine_{i,m} \geq min\_usage \cdot (y_i), \quad \forall i, m
\]
\[
y_i \in \{0, 1\} \quad \text{(binary variable indicating if oil $i$ is used in month $m$)}
\]
\[
y_j \geq dependency_{i,j} \cdot y_i, \quad \forall i,j
\]

\subsubsection*{Limitation on Oils per Month}
\[
\sum_{i=1}^{I} y_i \leq 3, \quad \forall m
\]

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Provided data in JSON format
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

#### Extract data from the provided structure
I = len(data['buy_price'])  #### Number of oil types
M = len(data['buy_price'][0])  #### Number of months

#### Create a problem variable
problem = pulp.LpProblem("Oil_Blend_Problem", pulp.LpMaximize)

#### Decision Variables
buy_quantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * buy_quantity[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))

problem += profit

#### Storage Dynamics
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buy_quantity[i][m] - refine[i][m]

for i in range(I):
    problem += storage[i][0] == data['init_amount']

#### Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= data['storage_size']

#### Refining Capacity
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

#### Final Product Hardness Condition
for m in range(M):
    problem += data['min_hardness'] <= pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5)
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5) <= data['max_hardness']

#### Initial and Final Storage Constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount']

#### Usage Requirements and Dependencies
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary'))

for i in range(I):
    for j in range(I):
        problem += pulp.LpVariable(f'y_{j}') >= data['dependencies'][i][j] * pulp.LpVariable(f'y_{i}')

#### Limitation on Oils per Month
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}') for i in range(I)) <= 3

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

