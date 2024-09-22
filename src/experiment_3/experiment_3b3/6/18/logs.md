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

\section*{Mathematical Model}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $buyquantity_{i,m}$: the amount of raw oil $i$ bought in month $m$.
    \item $refine_{i,m}$: the amount of raw oil $i$ refined in month $m$.
    \item $storage_{i,m}$: the amount of raw oil $i$ stored at the end of month $m$.
\end{itemize}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $price_{i,m}$: the buying price of oil $i$ in month $m$.
    \item $sell\_price$: the selling price of the final product per ton.
    \item $is\_vegetable_{i}$: a binary indicator for whether oil $i$ is vegetable.
    \item $max\_veg$: maximum tons of vegetable oils refined per month.
    \item $max\_non\_veg$: maximum tons of non-vegetable oils refined per month.
    \item $storage\_size$: the storage capacity for each raw oil.
    \item $storage\_cost$: the storage cost per ton per month.
    \item $max\_hardness$: the maximum allowable hardness of the final product.
    \item $min\_hardness$: the minimum allowable hardness of the final product.
    \item $hardness_{i}$: the hardness of oil $i$.
    \item $init\_amount$: initial amount of each type of raw oil in storage.
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}
1. **Storage constraints**:
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m} \quad \forall i, m
\]
\[
0 \leq storage_{i,m} \leq storage\_size \quad \forall i, m
\]

2. **Refining constraints**:
\[
\sum_{i \in vegetable} refine_{i,m} \leq max\_veg \quad \forall m
\]
\[
\sum_{i \in non\_vegetable} refine_{i,m} \leq max\_non\_veg \quad \forall m
\]

3. **Hardness constraints**:
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \forall m
\]

4. **Initial and final storage condition**:
\[
storage_{i,0} = init\_amount \quad \forall i
\]
\[
storage_{i,M} = init\_amount \quad \forall i
\]

5. **Non-negativity constraints**:
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

\section*{Mathematical Model}

\subsection*{Variables}
Let:
\begin{itemize}
    \item $buyquantity_{i,m}$: the amount of raw oil $i$ bought in month $m$.
    \item $refine_{i,m}$: the amount of raw oil $i$ refined in month $m$.
    \item $storage_{i,m}$: the amount of raw oil $i$ stored at the end of month $m$.
\end{itemize}

\subsection*{Parameters}
Let:
\begin{itemize}
    \item $price_{i,m}$: the buying price of oil $i$ in month $m$.
    \item $sell\_price$: the selling price of the final product per ton.
    \item $is\_vegetable_{i}$: a binary indicator for whether oil $i$ is vegetable.
    \item $max\_veg$: maximum tons of vegetable oils refined per month.
    \item $max\_non\_veg$: maximum tons of non-vegetable oils refined per month.
    \item $storage\_size$: the storage capacity for each raw oil.
    \item $storage\_cost$: the storage cost per ton per month.
    \item $max\_hardness$: the maximum allowable hardness of the final product.
    \item $min\_hardness$: the minimum allowable hardness of the final product.
    \item $hardness_{i}$: the hardness of oil $i$.
    \item $init\_amount$: initial amount of each type of raw oil in storage.
\end{itemize}

\subsection*{Objective Function}
Maximize profit:
\[
Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}
1. **Storage constraints**:
\[
storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m} \quad \forall i, m
\]
\[
0 \leq storage_{i,m} \leq storage\_size \quad \forall i, m
\]

2. **Refining constraints**:
\[
\sum_{i \in vegetable} refine_{i,m} \leq max\_veg \quad \forall m
\]
\[
\sum_{i \in non\_vegetable} refine_{i,m} \leq max\_non\_veg \quad \forall m
\]

3. **Hardness constraints**:
\[
min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \forall m
\]

4. **Initial and final storage condition**:
\[
storage_{i,0} = init\_amount \quad \forall i
\]
\[
storage_{i,M} = init\_amount \quad \forall i
\]

5. **Non-negativity constraints**:
\[
buyquantity_{i,m} \geq 0, \quad refine_{i,m} \geq 0, \quad storage_{i,m} \geq 0 \quad \forall i, m
\]

\end{document}</MATH_MODEL>
<DATA>
{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

#### Problem
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

#### Variables
buy_quantity = pulp.LpVariable.dicts("buyquantity",
                                     [(i, m) for i in range(data['I']) for m in range(data['M'])],
                                     lowBound=0, cat='Continuous')

refine = pulp.LpVariable.dicts("refine",
                               [(i, m) for i in range(data['I']) for m in range(data['M'])],
                               lowBound=0, cat='Continuous')

storage = pulp.LpVariable.dicts("storage",
                                [(i, m) for i in range(data['I']) for m in range(data['M'] + 1)],
                                lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum([
    data['SellPrice'] * pulp.lpSum(refine[i, m] for i in range(data['I'])) -
    pulp.lpSum(data['BuyPrice'][m][i] * buy_quantity[i, m] for i in range(data['I'])) -
    data['StorageCost'] * pulp.lpSum(storage[i, m + 1] for i in range(data['I']))
    for m in range(data['M'])
]), "Total_Profit"

#### Constraints

#### Initial storage condition
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], f"Initial_Storage_{i}"

#### Storage constraints
for i in range(data['I']):
    for m in range(1, data['M'] + 1):
        problem += storage[i, m] == storage[i, m - 1] + buy_quantity[i, m - 1] - refine[i, m - 1], f"Storage_Flow_{i}_{m}"
        problem += storage[i, m] <= data['StorageSize'], f"Max_Storage_{i}_{m}"

#### Refining constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"Max_Vegetable_Refining_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"Max_Non_Vegetable_Refining_{m}"

#### Hardness constraints
for m in range(data['M']):
    total_refined = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) >= data['MinHardness'] * total_refined, f"Min_Hardness_{m}"
    problem += pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) <= data['MaxHardness'] * total_refined, f"Max_Hardness_{m}"

#### Final storage condition
for i in range(data['I']):
    problem += storage[i, data['M']] == data['InitialAmount'], f"Final_Storage_{i}"

#### Solve
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

