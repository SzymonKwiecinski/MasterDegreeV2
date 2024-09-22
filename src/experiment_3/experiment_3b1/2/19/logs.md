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

\section*{Linear Programming Model for Oil Refining and Blending}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( buyquantity_{i,m} \) be the amount of oil \( i \) bought in month \( m \).
    \item \( refine_{i,m} \) be the amount of oil \( i \) refined in month \( m \).
    \item \( storage_{i,m} \) be the amount of oil \( i \) stored at the end of month \( m \).
\end{itemize}

\subsection*{Parameters}
Define the following parameters:
\begin{itemize}
    \item \( price_{i,m} \): Price of oil \( i \) in month \( m \).
    \item \( sell\_price \): Selling price per ton of the final product.
    \item \( max\_veg \): Maximum tons of vegetable oils refined per month.
    \item \( max\_non\_veg \): Maximum tons of non-vegetable oils refined per month.
    \item \( storage\_size \): Maximum tons of each raw oil that can be stored.
    \item \( storage\_cost \): Cost of storage per ton per month.
    \item \( max\_hardness \): Maximum allowable hardness of the final product.
    \item \( min\_hardness \): Minimum allowable hardness of the final product.
    \item \( hardness_{i} \): Hardness of oil \( i \).
    \item \( init\_amount \): Initial amount of each type of raw oil in storage.
    \item \( min\_usage \): Minimum tons of each oil that must be used if the oil is selected.
    \item \( dependency_{i,j} \): Dependency matrix indicating oil usage relations.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit given by:
\[
\text{Profit} = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} (price_{i,m} \cdot buyquantity_{i,m} + storage\_cost \cdot storage_{i,m}) \right)
\]

\subsection*{Constraints}

\textbf{1. Storage Balance:}
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m} \quad \forall i, m
\]
\[
storage_{i,0} = init\_amount \quad \forall i
\]
\[
storage_{i,M} = init\_amount \quad \forall i
\]

\textbf{2. Refining Limits:}
\[
\sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg \quad \forall m
\]
\[
\sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_non\_veg \quad \forall m
\]

\textbf{3. Hardness Constraints:}
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \forall m
\]

\textbf{4. Usage Minimum:}
If oil \( i \) is used (\( refine_{i,m} > 0 \)), then:
\[
refine_{i,m} \geq min\_usage \quad \forall i, m
\]

\textbf{5. Dependency Constraints:}
If \( dependency_{i,j} = 1 \) and \( refine_{i,m} > 0 \), then:
\[
refine_{j,m} \geq min\_usage \quad \forall j \text{ such that } dependency_{i,j} = 1, m
\]

\textbf{6. Oil Selection Limit:}
At most three different oils can be used in any month:
\[
\sum_{i=1}^{I} \text{if } refine_{i,m} > 0 \leq 3 \quad \forall m
\]

\subsection*{Non-negativity Constraints:}
\[
buyquantity_{i,m} \geq 0, \quad refine_{i,m} \geq 0, \quad storage_{i,m} \geq 0 \quad \forall i, m
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

\section*{Linear Programming Model for Oil Refining and Blending}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( buyquantity_{i,m} \) be the amount of oil \( i \) bought in month \( m \).
    \item \( refine_{i,m} \) be the amount of oil \( i \) refined in month \( m \).
    \item \( storage_{i,m} \) be the amount of oil \( i \) stored at the end of month \( m \).
\end{itemize}

\subsection*{Parameters}
Define the following parameters:
\begin{itemize}
    \item \( price_{i,m} \): Price of oil \( i \) in month \( m \).
    \item \( sell\_price \): Selling price per ton of the final product.
    \item \( max\_veg \): Maximum tons of vegetable oils refined per month.
    \item \( max\_non\_veg \): Maximum tons of non-vegetable oils refined per month.
    \item \( storage\_size \): Maximum tons of each raw oil that can be stored.
    \item \( storage\_cost \): Cost of storage per ton per month.
    \item \( max\_hardness \): Maximum allowable hardness of the final product.
    \item \( min\_hardness \): Minimum allowable hardness of the final product.
    \item \( hardness_{i} \): Hardness of oil \( i \).
    \item \( init\_amount \): Initial amount of each type of raw oil in storage.
    \item \( min\_usage \): Minimum tons of each oil that must be used if the oil is selected.
    \item \( dependency_{i,j} \): Dependency matrix indicating oil usage relations.
\end{itemize}

\subsection*{Objective Function}
Maximize the profit given by:
\[
\text{Profit} = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} (price_{i,m} \cdot buyquantity_{i,m} + storage\_cost \cdot storage_{i,m}) \right)
\]

\subsection*{Constraints}

\textbf{1. Storage Balance:}
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m} \quad \forall i, m
\]
\[
storage_{i,0} = init\_amount \quad \forall i
\]
\[
storage_{i,M} = init\_amount \quad \forall i
\]

\textbf{2. Refining Limits:}
\[
\sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg \quad \forall m
\]
\[
\sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_non\_veg \quad \forall m
\]

\textbf{3. Hardness Constraints:}
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \forall m
\]

\textbf{4. Usage Minimum:}
If oil \( i \) is used (\( refine_{i,m} > 0 \)), then:
\[
refine_{i,m} \geq min\_usage \quad \forall i, m
\]

\textbf{5. Dependency Constraints:}
If \( dependency_{i,j} = 1 \) and \( refine_{i,m} > 0 \), then:
\[
refine_{j,m} \geq min\_usage \quad \forall j \text{ such that } dependency_{i,j} = 1, m
\]

\textbf{6. Oil Selection Limit:}
At most three different oils can be used in any month:
\[
\sum_{i=1}^{I} \text{if } refine_{i,m} > 0 \leq 3 \quad \forall m
\]

\subsection*{Non-negativity Constraints:}
\[
buyquantity_{i,m} \geq 0, \quad refine_{i,m} \geq 0, \quad storage_{i,m} \geq 0 \quad \forall i, m
\]

\end{document}</MATH_MODEL>
<DATA>
{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('''{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')

#### Parameters
I = len(data['buy_price'])    #### Number of oil types
M = len(data['buy_price'][0]) #### Number of months
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
sell_price = data['sell_price']
storage_cost = data['storage_cost']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
dependencies = data['dependencies']

#### Create the problem
problem = pulp.LpProblem("Oil Refining and Blending", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M))
problem += profit

#### Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

    problem += storage[i, M-1] == init_amount  #### Final month storage constraint

#### Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness']

#### Usage Minimum
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * (1 if pulp.lpSum(refine[j, m] for j in range(I) if refine[j, m] > 0) > 0 else 0)

#### Dependency Constraints
for i in range(I):
    for m in range(M):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[j, m] >= min_usage * (1 if refine[i, m] > 0 else 0)

#### Oil Selection Limit
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

#### Solve the problem
problem.solve()

#### Output the objective value
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

#### Load data
data = json.loads('''{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')

#### Parameters
I = len(data['buy_price'])    #### Number of oil types
M = len(data['buy_price'][0]) #### Number of months
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
sell_price = data['sell_price']
storage_cost = data['storage_cost']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
dependencies = data['dependencies']

#### Create the problem
problem = pulp.LpProblem("Oil Refining and Blending", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M))
problem += profit

#### Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

    problem += storage[i, M-1] == init_amount  #### Final month storage constraint

#### Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness']

#### Usage Minimum
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * (1 if pulp.lpSum(refine[j, m] for j in range(I) if refine[j, m] > 0) > 0 else 0)

#### Dependency Constraints
for i in range(I):
    for m in range(M):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[j, m] >= min_usage * (1 if refine[i, m] > 0 else 0)

#### Oil Selection Limit
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/2/19/python_code0.py", line 5, in <module>
    data = json.loads('''{'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'sell_price': 150, 'is_vegetable': [True, True, False, False, False], 'max_vegetable_refining_per_month': 200, 'max_non_vegetable_refining_per_month': 250, 'storage_size': 1000, 'storage_cost': 5, 'min_hardness': 3, 'max_hardness': 6, 'hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'init_amount': 500, 'min_usage': 20, 'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('''{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')

#### Parameters
I = len(data['buy_price'])    #### Number of oil types
M = len(data['buy_price'][0]) #### Number of months
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
sell_price = data['sell_price']
storage_cost = data['storage_cost']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
dependencies = data['dependencies']

#### Create the problem
problem = pulp.LpProblem("Oil Refining and Blending", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(sell_price * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + storage_cost * storage[i, m] for i in range(I) for m in range(M))
problem += profit

#### Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

    problem += storage[i, M-1] == init_amount  #### Final month storage constraint

#### Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(hardness[i] * refine[i, m] for i in range(I)) / pulp.lpSum(refine[i, m] for i in range(I)) <= data['max_hardness']

#### Usage Minimum
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= min_usage * (1 if pulp.lpSum(refine[j, m] for j in range(I) if refine[j, m] > 0) > 0 else 0)

#### Dependency Constraints
for i in range(I):
    for m in range(M):
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += refine[j, m] >= min_usage * (1 if refine[i, m] > 0 else 0)

#### Oil Selection Limit
for m in range(M):
    problem += pulp.lpSum(1 for i in range(I) if refine[i, m] > 0) <= 3

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

