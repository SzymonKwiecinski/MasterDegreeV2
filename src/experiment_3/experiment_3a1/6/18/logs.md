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

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of different oils
    \item $M$: Number of months
    \item $price_{i,m}$: Buying price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Indicator variable for oil $i$ (1 if vegetable, 0 if non-vegetable)
    \item $max\_veg$: Maximum tons of vegetable oils that can be refined per month
    \item $max\_veg$: Maximum tons of non-vegetable oils that can be refined per month
    \item $storage\_size$: Maximum storage size for each oil
    \item $storage\_cost$: Cost of storage for each ton per month
    \item $max\_hardness$: Maximum allowable hardness of the final product
    \item $min\_hardness$: Minimum allowable hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial amount of each type of raw oil in storage
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} \sum_{m=1}^{M} price_{i,m} \cdot buyquantity_{i,m} - \sum_{i=1}^{I} storage\_cost \cdot storage_{i,m} \right)
\]

\subsection*{Constraints}

\begin{enumerate}

    \item \textbf{Refining Limits}:
    \[
    \sum_{i: is\_vegetable_i=1} refine_{i,m} \leq max\_veg, \quad \forall m
    \]
    \[
    \sum_{i: is\_vegetable_i=0} refine_{i,m} \leq max\_veg, \quad \forall m
    \]

    \item \textbf{Storage Capacity}:
    \[
    storage_{i,m} \leq storage\_size, \quad \forall i, m
    \]

    \item \textbf{Hardness Constraint}:
    \[
    \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \text{and} \quad \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \geq min\_hardness, \quad \forall m}
    \]

    \item \textbf{Storage Dynamics}:
    \[
    storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m > 0
    \]

    \item \textbf{Initial and Final Storage Constraints}:
    \[
    storage_{i,0} = init\_amount, \quad \forall i
    \]
    \[
    storage_{i,M} = init\_amount, \quad \forall i
    \]

\end{enumerate}

\subsection*{Output Format}
\begin{itemize}
    \item $buy$: A matrix $[buyquantity_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $refine$: A matrix $[refine_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $storage$: A matrix $[storage_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
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

\section*{Linear Programming Model for Oil Refining and Blending}

\subsection*{Parameters}
\begin{itemize}
    \item $I$: Number of different oils
    \item $M$: Number of months
    \item $price_{i,m}$: Buying price of oil $i$ in month $m$
    \item $sell\_price$: Selling price of the final product per ton
    \item $is\_vegetable_{i}$: Indicator variable for oil $i$ (1 if vegetable, 0 if non-vegetable)
    \item $max\_veg$: Maximum tons of vegetable oils that can be refined per month
    \item $max\_veg$: Maximum tons of non-vegetable oils that can be refined per month
    \item $storage\_size$: Maximum storage size for each oil
    \item $storage\_cost$: Cost of storage for each ton per month
    \item $max\_hardness$: Maximum allowable hardness of the final product
    \item $min\_hardness$: Minimum allowable hardness of the final product
    \item $hardness_{i}$: Hardness of oil $i$
    \item $init\_amount$: Initial amount of each type of raw oil in storage
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $buyquantity_{i,m}$: Amount of oil $i$ bought in month $m$
    \item $refine_{i,m}$: Amount of oil $i$ refined in month $m$
    \item $storage_{i,m}$: Amount of oil $i$ stored at the end of month $m$
\end{itemize}

\subsection*{Objective Function}
Maximize the profit:
\[
\text{Maximize } Z = \sum_{m=1}^{M} \left( sell\_price \cdot \sum_{i=1}^{I} refine_{i,m} - \sum_{i=1}^{I} \sum_{m=1}^{M} price_{i,m} \cdot buyquantity_{i,m} - \sum_{i=1}^{I} storage\_cost \cdot storage_{i,m} \right)
\]

\subsection*{Constraints}

\begin{enumerate}

    \item \textbf{Refining Limits}:
    \[
    \sum_{i: is\_vegetable_i=1} refine_{i,m} \leq max\_veg, \quad \forall m
    \]
    \[
    \sum_{i: is\_vegetable_i=0} refine_{i,m} \leq max\_veg, \quad \forall m
    \]

    \item \textbf{Storage Capacity}:
    \[
    storage_{i,m} \leq storage\_size, \quad \forall i, m
    \]

    \item \textbf{Hardness Constraint}:
    \[
    \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \leq max\_hardness \quad \text{and} \quad \frac{\sum_{i=1}^{I} hardness_{i} \cdot refine_{i,m}}{\sum_{i=1}^{I} refine_{i,m}} \geq min\_hardness, \quad \forall m}
    \]

    \item \textbf{Storage Dynamics}:
    \[
    storage_{i,m} = storage_{i,m-1} + buyquantity_{i,m} - refine_{i,m}, \quad \forall i, m > 0
    \]

    \item \textbf{Initial and Final Storage Constraints}:
    \[
    storage_{i,0} = init\_amount, \quad \forall i
    \]
    \[
    storage_{i,M} = init\_amount, \quad \forall i
    \]

\end{enumerate}

\subsection*{Output Format}
\begin{itemize}
    \item $buy$: A matrix $[buyquantity_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $refine$: A matrix $[refine_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
    \item $storage$: A matrix $[storage_{i,m}]$ for $i = 1, \ldots, I$ and $m = 1, \ldots, M$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
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
problem = pulp.LpProblem("Oil_Refining_and_Blend_Problem", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

#### Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
                    pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I)) - 
                    pulp.lpSum(storage_cost * storage[i][m] for i in range(I)) 
                    for m in range(M))

problem += profit, "Total_Profit"

#### Constraints
#### Refining Limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

#### Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= storage_size

#### Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) <= max_hardness
    problem += pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) >= min_hardness

#### Storage Dynamics
for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

#### Initial and Final Storage Constraints
for i in range(I):
    problem += storage[i][0] == init_amount
    problem += storage[i][M-1] == init_amount

#### Solve the problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

