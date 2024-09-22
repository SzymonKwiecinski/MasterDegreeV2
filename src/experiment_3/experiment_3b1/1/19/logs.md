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

\section*{Mathematical Model for the Food Manufacturing Problem}

\subsection*{Parameters}
\begin{align*}
& I: \text{Number of different oils} \\
& M: \text{Number of months} \\
& \text{price}_{i,m}: \text{Price of oil } i \text{ in month } m \\
& \text{sell\_price}: \text{Selling price per ton of the final product} \\
& \text{max\_veg}: \text{Maximum vegetable oils refining capacity per month} \\
& \text{max\_non\_veg}: \text{Maximum non-vegetable oils refining capacity per month} \\
& \text{storage\_size}: \text{Maximum storage capacity per oil} \\
& \text{storage\_cost}: \text{Cost of storage per ton per month} \\
& \text{max\_hardness}: \text{Maximum allowed hardness of the final product} \\
& \text{min\_hardness}: \text{Minimum allowed hardness of the final product} \\
& \text{hardness}_{i}: \text{Hardness of oil } i \\
& \text{init\_amount}: \text{Initial amount of each type of oil} \\
& \text{min\_usage}: \text{Minimum usage amount for an oil if it is used} \\
& \text{dependency}_{i,j}: \text{Dependency of oil } j \text{ on oil } i \\
& \text{is\_veg}_{i}: \text{Indicator for vegetable oil (1) or non-vegetable oil (0)} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{buyquantity}_{i,m}: \text{Amount of oil } i \text{ bought in month } m \\
& \text{refine}_{i,m}: \text{Amount of oil } i \text{ refined in month } m \\
& \text{storage}_{i,m}: \text{Amount of oil } i \text{ stored at the end of month } m \\
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buyquantity}_{i,m} \cdot \text{price}_{i,m} - \sum_{i=1}^{I} \text{storage}_{i,m} \cdot \text{storage\_cost} \right)
\]

\subsection*{Constraints}
1. **Storage Constraint**:
\[
\text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, m
\]

2. **Initial Storage**:
\[
\text{storage}_{i,0} = \text{init\_amount}, \quad \forall i
\]

3. **Final Storage**:
\[
\text{storage}_{i,M} = \text{init\_amount}, \quad \forall i
\]

4. **Refining Capacity**:
\[
\sum_{\text{is\_veg}_{i}=1} \text{refine}_{i,m} \leq \text{max\_veg}, \quad \forall m
\]
\[
\sum_{\text{is\_veg}_{i}=0} \text{refine}_{i,m} \leq \text{max\_non\_veg}, \quad \forall m
\]

5. **Hardness Constraint**:
\[
\text{max\_hardness} \geq \frac{\sum_{i=1}^{I} \text{hardness}_{i} \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \geq \text{min\_hardness}, \quad \forall m
\]

6. **Oil Usage Constraints**:
   - At least \text{min\_usage} must be used if an oil is used:
\[
\text{refine}_{i,m} \geq \text{min\_usage} \cdot y_{i,m}, \quad \forall i, m
\]
   - A binary variable \( y_{i,m} \) is defined as:
\[
y_{i,m} = 
\begin{cases} 
1 & \text{if refining oil } i \text{ in month } m \\
0 & \text{otherwise}
\end{cases}
\]

7. **Dependency Constraint**:
If oil \( i \) is used, all dependent oils \( j \) must also be used:
\[
\text{refine}_{j,m} \geq \text{min\_usage} \cdot (y_{i,m} + y_{j,m} - 1), \quad \forall i, j \text{ such that } \text{dependency}_{i,j} = 1, m
\]

8. **Limit on the number of oils**:
\[
\sum_{i=1}^{I} y_{i,m} \leq 3, \quad \forall m
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

\section*{Mathematical Model for the Food Manufacturing Problem}

\subsection*{Parameters}
\begin{align*}
& I: \text{Number of different oils} \\
& M: \text{Number of months} \\
& \text{price}_{i,m}: \text{Price of oil } i \text{ in month } m \\
& \text{sell\_price}: \text{Selling price per ton of the final product} \\
& \text{max\_veg}: \text{Maximum vegetable oils refining capacity per month} \\
& \text{max\_non\_veg}: \text{Maximum non-vegetable oils refining capacity per month} \\
& \text{storage\_size}: \text{Maximum storage capacity per oil} \\
& \text{storage\_cost}: \text{Cost of storage per ton per month} \\
& \text{max\_hardness}: \text{Maximum allowed hardness of the final product} \\
& \text{min\_hardness}: \text{Minimum allowed hardness of the final product} \\
& \text{hardness}_{i}: \text{Hardness of oil } i \\
& \text{init\_amount}: \text{Initial amount of each type of oil} \\
& \text{min\_usage}: \text{Minimum usage amount for an oil if it is used} \\
& \text{dependency}_{i,j}: \text{Dependency of oil } j \text{ on oil } i \\
& \text{is\_veg}_{i}: \text{Indicator for vegetable oil (1) or non-vegetable oil (0)} \\
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& \text{buyquantity}_{i,m}: \text{Amount of oil } i \text{ bought in month } m \\
& \text{refine}_{i,m}: \text{Amount of oil } i \text{ refined in month } m \\
& \text{storage}_{i,m}: \text{Amount of oil } i \text{ stored at the end of month } m \\
\end{align*}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Profit} = \sum_{m=1}^{M} \left( \text{sell\_price} \cdot \sum_{i=1}^{I} \text{refine}_{i,m} - \sum_{i=1}^{I} \text{buyquantity}_{i,m} \cdot \text{price}_{i,m} - \sum_{i=1}^{I} \text{storage}_{i,m} \cdot \text{storage\_cost} \right)
\]

\subsection*{Constraints}
1. **Storage Constraint**:
\[
\text{storage}_{i,m} = \text{storage}_{i,m-1} + \text{buyquantity}_{i,m} - \text{refine}_{i,m}, \quad \forall i, m
\]

2. **Initial Storage**:
\[
\text{storage}_{i,0} = \text{init\_amount}, \quad \forall i
\]

3. **Final Storage**:
\[
\text{storage}_{i,M} = \text{init\_amount}, \quad \forall i
\]

4. **Refining Capacity**:
\[
\sum_{\text{is\_veg}_{i}=1} \text{refine}_{i,m} \leq \text{max\_veg}, \quad \forall m
\]
\[
\sum_{\text{is\_veg}_{i}=0} \text{refine}_{i,m} \leq \text{max\_non\_veg}, \quad \forall m
\]

5. **Hardness Constraint**:
\[
\text{max\_hardness} \geq \frac{\sum_{i=1}^{I} \text{hardness}_{i} \cdot \text{refine}_{i,m}}{\sum_{i=1}^{I} \text{refine}_{i,m}} \geq \text{min\_hardness}, \quad \forall m
\]

6. **Oil Usage Constraints**:
   - At least \text{min\_usage} must be used if an oil is used:
\[
\text{refine}_{i,m} \geq \text{min\_usage} \cdot y_{i,m}, \quad \forall i, m
\]
   - A binary variable \( y_{i,m} \) is defined as:
\[
y_{i,m} = 
\begin{cases} 
1 & \text{if refining oil } i \text{ in month } m \\
0 & \text{otherwise}
\end{cases}
\]

7. **Dependency Constraint**:
If oil \( i \) is used, all dependent oils \( j \) must also be used:
\[
\text{refine}_{j,m} \geq \text{min\_usage} \cdot (y_{i,m} + y_{j,m} - 1), \quad \forall i, j \text{ such that } \text{dependency}_{i,j} = 1, m
\]

8. **Limit on the number of oils**:
\[
\sum_{i=1}^{I} y_{i,m} \leq 3, \quad \forall m
\]

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

#### Parameters
I = len(data['buy_price'])  #### Number of different oils
M = len(data['buy_price'][0])  #### Number of months

#### Create the problem
problem = pulp.LpProblem("Food_Manufacturing_Profit_Optimization", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(buyquantity[i, m] * data['buy_price'][i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(storage[i, m] * data['storage_cost'] for i in range(I) for m in range(M))
problem += profit

#### Constraints
#### Initial Storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount'], f"Initial_Storage_{i}"

#### Final Storage
for i in range(I):
    problem += storage[i, M] == data['init_amount'], f"Final_Storage_{i}"

#### Storage Constraint
for m in range(1, M+1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1], f"Storage_Constraint_{i}_{m}"

#### Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"NonVegetable_Capacity_{m}"

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness'], f"Max_Hardness_{m}"
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness'], f"Min_Hardness_{m}"

#### Oil Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.LpVariable(f'y_{i}_{m}', cat='Binary'), f"Min_Usage_{i}_{m}"

#### Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j, m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary') + pulp.LpVariable(f'y_{j}_{m}', cat='Binary') - 1), f"Dependency_{i}_{j}_{m}"

#### Limit on the number of oils
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}', cat='Binary') for i in range(I)) <= 3, f"Oil_Limit_{m}"

#### Solve problem
problem.solve()

#### Output the result
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
import json

#### Data input
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

#### Parameters
I = len(data['buy_price'])  #### Number of different oils
M = len(data['buy_price'][0])  #### Number of months

#### Create the problem
problem = pulp.LpProblem("Food_Manufacturing_Profit_Optimization", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(buyquantity[i, m] * data['buy_price'][i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(storage[i, m] * data['storage_cost'] for i in range(I) for m in range(M))
problem += profit

#### Constraints
#### Initial Storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount'], f"Initial_Storage_{i}"

#### Final Storage
for i in range(I):
    problem += storage[i, M] == data['init_amount'], f"Final_Storage_{i}"

#### Storage Constraint
for m in range(1, M+1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1], f"Storage_Constraint_{i}_{m}"

#### Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"NonVegetable_Capacity_{m}"

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness'], f"Max_Hardness_{m}"
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness'], f"Min_Hardness_{m}"

#### Oil Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.LpVariable(f'y_{i}_{m}', cat='Binary'), f"Min_Usage_{i}_{m}"

#### Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j, m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary') + pulp.LpVariable(f'y_{j}_{m}', cat='Binary') - 1), f"Dependency_{i}_{j}_{m}"

#### Limit on the number of oils
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}', cat='Binary') for i in range(I)) <= 3, f"Oil_Limit_{m}"

#### Solve problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/1/19/python_code0.py", line 59, in <module>
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 2233, in lpSum
    return LpAffineExpression().addInPlace(vector)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 867, in addInPlace
    for e in other:
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/1/19/python_code0.py", line 59, in <genexpr>
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
                                                            ~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

#### Parameters
I = len(data['buy_price'])  #### Number of different oils
M = len(data['buy_price'][0])  #### Number of months

#### Create the problem
problem = pulp.LpProblem("Food_Manufacturing_Profit_Optimization", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(buyquantity[i, m] * data['buy_price'][i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(storage[i, m] * data['storage_cost'] for i in range(I) for m in range(M))
problem += profit

#### Constraints
#### Initial Storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount'], f"Initial_Storage_{i}"

#### Final Storage
for i in range(I):
    problem += storage[i, M] == data['init_amount'], f"Final_Storage_{i}"

#### Storage Constraint
for m in range(1, M+1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1], f"Storage_Constraint_{i}_{m}"

#### Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Vegetable_Capacity_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"NonVegetable_Capacity_{m}"

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-5) <= data['max_hardness'], f"Max_Hardness_{m}"
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) / (pulp.lpSum(refine[i, m] for i in range(I)) + 1e-5) >= data['min_hardness'], f"Min_Hardness_{m}"

#### Oil Usage Constraints
for m in range(M):
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.LpVariable(f'y_{i}_{m}', cat='Binary'), f"Min_Usage_{i}_{m}"

#### Dependency Constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j, m] >= data['min_usage'] * (pulp.LpVariable(f'y_{i}_{m}', cat='Binary') + pulp.LpVariable(f'y_{j}_{m}', cat='Binary') - 1), f"Dependency_{i}_{j}_{m}"

#### Limit on the number of oils
for m in range(M):
    problem += pulp.lpSum(pulp.LpVariable(f'y_{i}_{m}', cat='Binary') for i in range(I)) <= 3, f"Oil_Limit_{m}"

#### Solve problem
problem.solve()

#### Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

