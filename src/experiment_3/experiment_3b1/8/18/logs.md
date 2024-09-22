# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
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
    "init_amount": init_amount
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
\begin{align*}
& \text{Let } buyquantity_{i,m} \text{ be the amount of oil } i \text{ bought in month } m \\
& \text{Let } refine_{i,m} \text{ be the amount of oil } i \text{ refined in month } m \\
& \text{Let } storage_{i,m} \text{ be the amount of oil } i \text{ stored at the end of month } m \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
& I \text{ = number of different oils} \\
& M \text{ = number of months} \\
& price_{i,m} \text{ = purchase price of oil } i \text{ in month } m \\
& sell\_price \text{ = selling price of the final product per ton} \\
& max\_veg \text{ = maximum vegetable oils refining capacity per month} \\
& max\_non\_veg \text{ = maximum non-vegetable oils refining capacity per month} \\
& storage\_size \text{ = maximum storage capacity of each oil} \\
& storage\_cost \text{ = storage cost of each oil per ton per month} \\
& max\_hardness \text{ = maximum permissible hardness of the final product} \\
& min\_hardness \text{ = minimum permissible hardness of the final product} \\
& hardness_{i} \text{ = hardness value of oil } i \\
& init\_amount \text{ = initial amount of each oil in storage} \\
& is\_vegetable_{i} \text{ = indicator whether oil } i \text{ is vegetable (1) or non-vegetable (0)} \\
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize Profit: } Z &= \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} (price_{i,m} \cdot buyquantity_{i,m} + storage\_cost \cdot storage_{i,m}) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{1. Refining Capacities:} \\
& \sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg, \quad \forall m \in \{1, 2, \ldots, M\} \\
& \sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_non\_veg, \quad \forall m \in \{1, 2, \ldots, M\} \\

\text{2. Storage Constraints:} \\
& storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i \in \{1, 2, \ldots, I\}, \forall m \in \{1, 2, \ldots, M\} \\
& 0 \leq storage_{i,m} \leq storage\_size, \quad \forall i \in \{1, 2, \ldots, I\}, \forall m \in \{1, 2, \ldots, M\} \\

\text{3. Initial and Final Storage:} \\
& storage_{i,0} = init\_amount, \quad \forall i \in \{1, 2, \ldots, I\} \\
& storage_{i,M} = init\_amount, \quad \forall i \in \{1, 2, \ldots, I\} \\

\text{4. Hardness Constraints:} \\
& \min\_hardness \leq \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m \in \{1, 2, \ldots, M\}
\end{align*}

\subsection*{Output Format}
The output will be structured as follows:
\begin{align*}
& \text{"buy": } [[buyquantity_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M], \\
& \text{"refine": } [[refine_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M], \\
& \text{"storage": } [[storage_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M]
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

\section*{Linear Programming Model for Oil Refining and Blending}

\subsection*{Variables}
\begin{align*}
& \text{Let } buyquantity_{i,m} \text{ be the amount of oil } i \text{ bought in month } m \\
& \text{Let } refine_{i,m} \text{ be the amount of oil } i \text{ refined in month } m \\
& \text{Let } storage_{i,m} \text{ be the amount of oil } i \text{ stored at the end of month } m \\
\end{align*}

\subsection*{Parameters}
\begin{align*}
& I \text{ = number of different oils} \\
& M \text{ = number of months} \\
& price_{i,m} \text{ = purchase price of oil } i \text{ in month } m \\
& sell\_price \text{ = selling price of the final product per ton} \\
& max\_veg \text{ = maximum vegetable oils refining capacity per month} \\
& max\_non\_veg \text{ = maximum non-vegetable oils refining capacity per month} \\
& storage\_size \text{ = maximum storage capacity of each oil} \\
& storage\_cost \text{ = storage cost of each oil per ton per month} \\
& max\_hardness \text{ = maximum permissible hardness of the final product} \\
& min\_hardness \text{ = minimum permissible hardness of the final product} \\
& hardness_{i} \text{ = hardness value of oil } i \\
& init\_amount \text{ = initial amount of each oil in storage} \\
& is\_vegetable_{i} \text{ = indicator whether oil } i \text{ is vegetable (1) or non-vegetable (0)} \\
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize Profit: } Z &= \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} (price_{i,m} \cdot buyquantity_{i,m} + storage\_cost \cdot storage_{i,m}) \right)
\end{align*}

\subsection*{Constraints}
\begin{align*}
\text{1. Refining Capacities:} \\
& \sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg, \quad \forall m \in \{1, 2, \ldots, M\} \\
& \sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_non\_veg, \quad \forall m \in \{1, 2, \ldots, M\} \\

\text{2. Storage Constraints:} \\
& storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i \in \{1, 2, \ldots, I\}, \forall m \in \{1, 2, \ldots, M\} \\
& 0 \leq storage_{i,m} \leq storage\_size, \quad \forall i \in \{1, 2, \ldots, I\}, \forall m \in \{1, 2, \ldots, M\} \\

\text{3. Initial and Final Storage:} \\
& storage_{i,0} = init\_amount, \quad \forall i \in \{1, 2, \ldots, I\} \\
& storage_{i,M} = init\_amount, \quad \forall i \in \{1, 2, \ldots, I\} \\

\text{4. Hardness Constraints:} \\
& \min\_hardness \leq \frac{\sum_{i=1}^{I} (hardness_{i} \cdot refine_{i,m})}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m \in \{1, 2, \ldots, M\}
\end{align*}

\subsection*{Output Format}
The output will be structured as follows:
\begin{align*}
& \text{"buy": } [[buyquantity_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M], \\
& \text{"refine": } [[refine_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M], \\
& \text{"storage": } [[storage_{i, m} \text{ for } i = 1,\ldots,I] \text{ for } m = 1, \ldots, M]
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                 [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                 [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'SellPrice': 150,
    'IsVegetable': [True, True, False, False, False],
    'MaxVegetableRefiningPerMonth': 200,
    'MaxNonVegetableRefiningPerMonth': 250,
    'StorageSize': 1000,
    'StorageCost': 5,
    'MinHardness': 3,
    'MaxHardness': 6,
    'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'InitialAmount': 500
}

#### Initialize the LP problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

#### Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", 
                                     ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                     lowBound=0)
refine = pulp.LpVariable.dicts("refine", 
                                 ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                 lowBound=0)
storage = pulp.LpVariable.dicts("storage", 
                                  ((i, m) for i in range(data['I']) for m in range(data['M'] + 1)),
                                  lowBound=0, 
                                  upBound=data['StorageSize'])

#### Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(1, data['M'] + 1)) - \
            pulp.lpSum(data['BuyPrice'][m-1][i] * buyquantity[i, m] + data['StorageCost'] * storage[i, m] 
                       for i in range(data['I']) for m in range(1, data['M'] + 1)), "Total_Profit"

#### Constraints
for m in range(1, data['M'] + 1):
    #### Refining Capacities
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], "MaxVeg_Refining_%d" % m
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], "MaxNonVeg_Refining_%d" % m

    #### Storage Constraints
    for i in range(data['I']):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], "StorageBalance_%d_%d" % (i, m)
        problem += storage[i, m] >= 0, "NonNegativeStorage_%d_%d" % (i, m)
        problem += storage[i, m] <= data['StorageSize'], "StorageLimit_%d_%d" % (i, m)

#### Initial and Final Storage
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], "InitialStorage_%d" % i
    problem += storage[i, data['M']] == data['InitialAmount'], "FinalStorage_%d" % i

#### Hardness Constraints
for m in range(1, data['M'] + 1):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) >= data['MinHardness']), "MinHardness_%d" % m
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) <= data['MaxHardness']), "MaxHardness_%d" % m

#### Solve the problem
problem.solve()

#### Output the results
buy_result = [[pulp.value(buyquantity[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
refine_result = [[pulp.value(refine[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
storage_result = [[pulp.value(storage[i, m]) for i in range(data['I'])] for m in range(data['M'] + 1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

for key, value in output.items():
    print(f"{key}: {value}")

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

#### Data from the provided JSON format
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                 [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                 [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'SellPrice': 150,
    'IsVegetable': [True, True, False, False, False],
    'MaxVegetableRefiningPerMonth': 200,
    'MaxNonVegetableRefiningPerMonth': 250,
    'StorageSize': 1000,
    'StorageCost': 5,
    'MinHardness': 3,
    'MaxHardness': 6,
    'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'InitialAmount': 500
}

#### Initialize the LP problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

#### Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", 
                                     ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                     lowBound=0)
refine = pulp.LpVariable.dicts("refine", 
                                 ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                 lowBound=0)
storage = pulp.LpVariable.dicts("storage", 
                                  ((i, m) for i in range(data['I']) for m in range(data['M'] + 1)),
                                  lowBound=0, 
                                  upBound=data['StorageSize'])

#### Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(1, data['M'] + 1)) - \
            pulp.lpSum(data['BuyPrice'][m-1][i] * buyquantity[i, m] + data['StorageCost'] * storage[i, m] 
                       for i in range(data['I']) for m in range(1, data['M'] + 1)), "Total_Profit"

#### Constraints
for m in range(1, data['M'] + 1):
    #### Refining Capacities
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], "MaxVeg_Refining_%d" % m
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], "MaxNonVeg_Refining_%d" % m

    #### Storage Constraints
    for i in range(data['I']):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], "StorageBalance_%d_%d" % (i, m)
        problem += storage[i, m] >= 0, "NonNegativeStorage_%d_%d" % (i, m)
        problem += storage[i, m] <= data['StorageSize'], "StorageLimit_%d_%d" % (i, m)

#### Initial and Final Storage
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], "InitialStorage_%d" % i
    problem += storage[i, data['M']] == data['InitialAmount'], "FinalStorage_%d" % i

#### Hardness Constraints
for m in range(1, data['M'] + 1):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) >= data['MinHardness']), "MinHardness_%d" % m
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) <= data['MaxHardness']), "MaxHardness_%d" % m

#### Solve the problem
problem.solve()

#### Output the results
buy_result = [[pulp.value(buyquantity[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
refine_result = [[pulp.value(refine[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
storage_result = [[pulp.value(storage[i, m]) for i in range(data['I'])] for m in range(data['M'] + 1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

for key, value in output.items():
    print(f"{key}: {value}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/8/18/python_code0.py", line 62, in <module>
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 956, in __truediv__
    return self.__div__(other)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 943, in __div__
    raise TypeError(
TypeError: Expressions cannot be divided by a non-constant expression
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
The error message indicates that a division operation is attempting to divide by a variable expression, which is not allowed in the context of the `pulp` library. To fix the syntax error, we can introduce an auxiliary variable that represents the summation of the refining amounts for each iteration, and then use this variable in the division. Here is the corrected code:

```python
import pulp
import json

#### Data from the provided JSON format
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115],
                 [110, 140, 130, 100, 95], [120, 110, 120, 120, 125],
                 [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'SellPrice': 150,
    'IsVegetable': [True, True, False, False, False],
    'MaxVegetableRefiningPerMonth': 200,
    'MaxNonVegetableRefiningPerMonth': 250,
    'StorageSize': 1000,
    'StorageCost': 5,
    'MinHardness': 3,
    'MaxHardness': 6,
    'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'InitialAmount': 500
}

#### Initialize the LP problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

#### Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", 
                                     ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                     lowBound=0)
refine = pulp.LpVariable.dicts("refine", 
                                 ((i, m) for i in range(data['I']) for m in range(1, data['M'] + 1)),
                                 lowBound=0)
storage = pulp.LpVariable.dicts("storage", 
                                  ((i, m) for i in range(data['I']) for m in range(data['M'] + 1)),
                                  lowBound=0, 
                                  upBound=data['StorageSize'])

#### Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(1, data['M'] + 1)) - \
            pulp.lpSum(data['BuyPrice'][m-1][i] * buyquantity[i, m] + data['StorageCost'] * storage[i, m] 
                       for i in range(data['I']) for m in range(1, data['M'] + 1)), "Total_Profit"

#### Constraints
for m in range(1, data['M'] + 1):
    #### Refining Capacities
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], "MaxVeg_Refining_%d" % m
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], "MaxNonVeg_Refining_%d" % m

    #### Storage Constraints
    for i in range(data['I']):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], "StorageBalance_%d_%d" % (i, m)
        problem += storage[i, m] >= 0, "NonNegativeStorage_%d_%d" % (i, m)
        problem += storage[i, m] <= data['StorageSize'], "StorageLimit_%d_%d" % (i, m)

#### Initial and Final Storage
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], "InitialStorage_%d" % i
    problem += storage[i, data['M']] == data['InitialAmount'], "FinalStorage_%d" % i

#### Hardness Constraints
for m in range(1, data['M'] + 1):
    total_refined = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refined >= data['MinHardness']), "MinHardness_%d" % m
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refined <= data['MaxHardness']), "MaxHardness_%d" % m

#### Solve the problem
problem.solve()

#### Output the results
buy_result = [[pulp.value(buyquantity[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
refine_result = [[pulp.value(refine[i, m]) for i in range(data['I'])] for m in range(1, data['M'] + 1)]
storage_result = [[pulp.value(storage[i, m]) for i in range(data['I'])] for m in range(data['M'] + 1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

for key, value in output.items():
    print(f"{key}: {value}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

