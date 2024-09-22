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

\section*{Mathematical Model for Oil Refining and Blending}

\subsection*{Parameters}
\begin{align*}
& I: \text{Number of different oils} \\
& M: \text{Number of months} \\
& price_{i,m}: \text{Purchase price of oil } i \text{ in month } m \\
& sell\_price: \text{Selling price of the final product per ton} \\
& max\_veg: \text{Maximum refining capacity for vegetable oils per month} \\
& max\_veg: \text{Maximum refining capacity for non-vegetable oils per month} \\
& storage\_size: \text{Maximum storage size for each oil} \\
& storage\_cost: \text{Storage cost per ton per month} \\
& max\_hardness: \text{Maximum hardness of the final product} \\
& min\_hardness: \text{Minimum hardness of the final product} \\
& hardness_{i}: \text{Hardness of oil } i \\
& init\_amount: \text{Initial amount of each type of raw oil in storage}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& buyquantity_{i,m}: \text{Amount of oil } i \text{ bought in month } m \\
& refine_{i,m}: \text{Amount of oil } i \text{ refined in month } m \\
& storage_{i,m}: \text{Amount of oil } i \text{ stored in month } m
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize Profit} = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}

1. **Refining Capacity Constraints:**
   \[
   \sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg, \quad \forall m = 1,\ldots,M
   \]
   \[
   \sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_veg, \quad \forall m = 1,\ldots,M
   \]

2. **Storage Constraints:**
   \[
   storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i = 1,\ldots,I, \, \forall m = 1,\ldots,M
   \]
   \[
   0 \leq storage_{i,m} \leq storage\_size, \quad \forall i = 1,\ldots,I, \, \forall m = 1,\ldots,M
   \]

3. **Hardness Constraints:**
   \[
   min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m = 1,\ldots,M
   \]

4. **Initial and Final Storage Constraints:**
   \[
   storage_{i,0} = init\_amount, \quad \forall i = 1,\ldots,I
   \]
   \[
   storage_{i,M} = init\_amount, \quad \forall i = 1,\ldots,I
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

\section*{Mathematical Model for Oil Refining and Blending}

\subsection*{Parameters}
\begin{align*}
& I: \text{Number of different oils} \\
& M: \text{Number of months} \\
& price_{i,m}: \text{Purchase price of oil } i \text{ in month } m \\
& sell\_price: \text{Selling price of the final product per ton} \\
& max\_veg: \text{Maximum refining capacity for vegetable oils per month} \\
& max\_veg: \text{Maximum refining capacity for non-vegetable oils per month} \\
& storage\_size: \text{Maximum storage size for each oil} \\
& storage\_cost: \text{Storage cost per ton per month} \\
& max\_hardness: \text{Maximum hardness of the final product} \\
& min\_hardness: \text{Minimum hardness of the final product} \\
& hardness_{i}: \text{Hardness of oil } i \\
& init\_amount: \text{Initial amount of each type of raw oil in storage}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
& buyquantity_{i,m}: \text{Amount of oil } i \text{ bought in month } m \\
& refine_{i,m}: \text{Amount of oil } i \text{ refined in month } m \\
& storage_{i,m}: \text{Amount of oil } i \text{ stored in month } m
\end{align*}

\subsection*{Objective Function}
\[
\text{Maximize Profit} = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} price_{i,m} \cdot buyquantity_{i,m} - storage\_cost \cdot \sum_{i=1}^{I} storage_{i,m} \right)
\]

\subsection*{Constraints}

1. **Refining Capacity Constraints:**
   \[
   \sum_{i \in \text{veg}} refine_{i,m} \leq max\_veg, \quad \forall m = 1,\ldots,M
   \]
   \[
   \sum_{i \in \text{non-veg}} refine_{i,m} \leq max\_veg, \quad \forall m = 1,\ldots,M
   \]

2. **Storage Constraints:**
   \[
   storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i = 1,\ldots,I, \, \forall m = 1,\ldots,M
   \]
   \[
   0 \leq storage_{i,m} \leq storage\_size, \quad \forall i = 1,\ldots,I, \, \forall m = 1,\ldots,M
   \]

3. **Hardness Constraints:**
   \[
   min\_hardness \leq \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness, \quad \forall m = 1,\ldots,M
   \]

4. **Initial and Final Storage Constraints:**
   \[
   storage_{i,0} = init\_amount, \quad \forall i = 1,\ldots,I
   \]
   \[
   storage_{i,M} = init\_amount, \quad \forall i = 1,\ldots,I
   \]

\end{document}</MATH_MODEL>
<DATA>
{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data initialization
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

#### Create the problem
problem = pulp.LpProblem("OilRefiningAndBlending", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

#### Objective Function
problem += pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) - \
                     pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) - \
                     storage_cost * pulp.lpSum(storage[i][m] for i in range(I) for m in range(M))

#### Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

for m in range(M):
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == init_amount
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]
        
        problem += storage[i][m] <= storage_size
        problem += storage[i][m] >= 0
        
for m in range(M):
    refine_total = pulp.lpSum(refine[i][m] for i in range(I))
    problem += (min_hardness * refine_total <= 
                pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) <= 
                max_hardness * refine_total)

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

