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

\textbf{Indices:}
\begin{itemize}
    \item $i$: Index for oils, where $i = 1, 2, \ldots, I$
    \item $m$: Index for months, where $m = 0, 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $price_{i,m}$: Buying price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Boolean indicating whether oil $i$ is vegetable
    \item $max\_vegetable\_refining\_per\_month$: Max tons of vegetable oils refined per month
    \item $max\_non\_vegetable\_refining\_per\_month$: Max tons of non-vegetable oils refined per month
    \item $storage\_size$: Max tons of each raw oil that can be stored
    \item $storage\_cost$: Cost of storage per ton per month
    \item $max\_hardness$: Max hardness of the final product
    \item $min\_hardness$: Min hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial amount of each type of raw oil in storage
    \item $min\_usage$: Minimum usage of each oil when used
    \item $dependency_{i,j}$: Dependency relation between oils
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - \sum_{i=1}^{I} storage\_cost \cdot storage_{i,m} \right)
\]

\textbf{Subject to:}

1. **Storage Balance:**
   \[
   storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, \forall m \text{ except } m=0
   \]
   \[
   storage_{i,0} = init\_amount, \quad \forall i
   \]

2. **Storage Capacity:**
   \[
   storage_{i,m} \leq storage\_size, \quad \forall i, \forall m
   \]

3. **Refining Capacity:**
   \[
   \sum_{i \in I_{veg}} refine_{i,m} \leq max\_vegetable\_refining\_per\_month, \quad \forall m
   \]
   \[
   \sum_{i \in I_{non-veg}} refine_{i,m} \leq max\_non\_vegetable\_refining\_per\_month, \quad \forall m
   \]

4. **Hardness Constraint:**
   \[
   \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \in [min\_hardness, max\_hardness], \quad \forall m
   \]

5. **Initial and Final Storage:**
   \[
   storage_{i,M} = init\_amount, \quad \forall i
   \]

6. **Oil Usage:**
   If oil $i$ is used in month $m$:
   \[
   refine_{i,m} \geq min\_usage \cdot y_{i,m}, \quad \forall i, \forall m
   \]
   where $y_{i,m}$ is a binary variable indicating whether oil $i$ is refined in month $m$.

7. **Dependency Constraints:**
   \[
   refine_{j,m} \leq dependency_{i,j} \cdot \sum_{k=1}^{I} refine_{k,m}, \quad \forall i, j \text{ where } dependency_{i,j} = 1
   \]

8. **Maximum Oils Used:**
   \[
   \sum_{i=1}^{I} y_{i,m} \leq 3, \quad \forall m
   \]

9. **Non-negativity:**
   \[
   buyquantity_{i,m} \geq 0, \quad refine_{i,m} \geq 0, \quad storage_{i,m} \geq 0, \quad \forall i, m
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

\section*{Mathematical Model}

\textbf{Indices:}
\begin{itemize}
    \item $i$: Index for oils, where $i = 1, 2, \ldots, I$
    \item $m$: Index for months, where $m = 0, 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $price_{i,m}$: Buying price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Boolean indicating whether oil $i$ is vegetable
    \item $max\_vegetable\_refining\_per\_month$: Max tons of vegetable oils refined per month
    \item $max\_non\_vegetable\_refining\_per\_month$: Max tons of non-vegetable oils refined per month
    \item $storage\_size$: Max tons of each raw oil that can be stored
    \item $storage\_cost$: Cost of storage per ton per month
    \item $max\_hardness$: Max hardness of the final product
    \item $min\_hardness$: Min hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial amount of each type of raw oil in storage
    \item $min\_usage$: Minimum usage of each oil when used
    \item $dependency_{i,j}$: Dependency relation between oils
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - \sum_{i=1}^{I} storage\_cost \cdot storage_{i,m} \right)
\]

\textbf{Subject to:}

1. **Storage Balance:**
   \[
   storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, \forall m \text{ except } m=0
   \]
   \[
   storage_{i,0} = init\_amount, \quad \forall i
   \]

2. **Storage Capacity:**
   \[
   storage_{i,m} \leq storage\_size, \quad \forall i, \forall m
   \]

3. **Refining Capacity:**
   \[
   \sum_{i \in I_{veg}} refine_{i,m} \leq max\_vegetable\_refining\_per\_month, \quad \forall m
   \]
   \[
   \sum_{i \in I_{non-veg}} refine_{i,m} \leq max\_non\_vegetable\_refining\_per\_month, \quad \forall m
   \]

4. **Hardness Constraint:**
   \[
   \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \in [min\_hardness, max\_hardness], \quad \forall m
   \]

5. **Initial and Final Storage:**
   \[
   storage_{i,M} = init\_amount, \quad \forall i
   \]

6. **Oil Usage:**
   If oil $i$ is used in month $m$:
   \[
   refine_{i,m} \geq min\_usage \cdot y_{i,m}, \quad \forall i, \forall m
   \]
   where $y_{i,m}$ is a binary variable indicating whether oil $i$ is refined in month $m$.

7. **Dependency Constraints:**
   \[
   refine_{j,m} \leq dependency_{i,j} \cdot \sum_{k=1}^{I} refine_{k,m}, \quad \forall i, j \text{ where } dependency_{i,j} = 1
   \]

8. **Maximum Oils Used:**
   \[
   \sum_{i=1}^{I} y_{i,m} \leq 3, \quad \forall m
   \]

9. **Non-negativity:**
   \[
   buyquantity_{i,m} \geq 0, \quad refine_{i,m} \geq 0, \quad storage_{i,m} \geq 0, \quad \forall i, m
   \]

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

#### Indices
I = len(data['buy_price'])  #### Number of oils
M = len(data['buy_price'][0]) - 1  #### Number of months excluding month 0

#### Create the LP problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((i, m) for i in range(I) for m in range(M+1)), cat='Binary')

#### Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(1, M+1)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M+1)) - \
         pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M+1))

problem += profit

#### Constraints

#### Storage Balance
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
    problem += storage[i, 0] == data['init_amount']

#### Storage Capacity
for i in range(I):
    for m in range(M+1):
        problem += storage[i, m] <= data['storage_size']

#### Refining Capacity
for m in range(M+1):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

#### Hardness Constraint
for m in range(1, M+1):
    hardness_expr = pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I))
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    problem += (hardness_expr / total_refine >= data['min_hardness']) if total_refine > 0 else 0
    problem += (hardness_expr / total_refine <= data['max_hardness']) if total_refine > 0 else 0

#### Initial and Final Storage
for i in range(I):
    problem += storage[i, M] == data['init_amount']

#### Oil Usage
for i in range(I):
    for m in range(1, M+1):
        problem += refine[i, m] >= data['min_usage'] * y[i, m]

#### Dependency Constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(1, M+1):
                problem += refine[j, m] <= pulp.lpSum(refine[k, m] for k in range(I))

#### Maximum Oils Used
for m in range(M+1):
    problem += pulp.lpSum(y[i, m] for i in range(I)) <= 3

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

