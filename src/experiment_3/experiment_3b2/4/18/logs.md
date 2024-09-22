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
To formulate a mathematical model for this problem, we can define a Linear Programming (LP) model. The goal is to maximize the profit by determining the optimal quantities to buy, store and refine for each type of oil in each month while adhering to the given constraints.

Let's define the variables and constraints as needed in this problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let:
\begin{align*}
  & \text{buyquantity}_{i, m} \quad \text{be the quantity of oil $i$ bought in month $m$.} \\
  & \text{refine}_{i, m} \quad \text{be the quantity of oil $i$ refined in month $m$.} \\
  & \text{storage}_{i, m} \quad \text{be the quantity of oil $i$ stored at the end of month $m$.}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit over the planning horizon:
\begin{align*}
  \text{Maximize} \quad 
  & \sum_{m=1}^{M} \sum_{i=1}^{I} \left[ (\text{sell\_price} \cdot \text{refine}_{i, m}) - (\text{buy\_price}_{i, m} \cdot \text{buyquantity}_{i, m}) - (\text{storage\_cost} \cdot \text{storage}_{i, m}) \right]
\end{align*}

\subsection*{Constraints}
\begin{align*}
  & \text{For each oil } i \text{ and month } m: \\
  & \text{storage}_{i, m} = \text{storage}_{i, m-1} + \text{buyquantity}_{i, m} - \text{refine}_{i, m} \quad \forall i, m \\
  & \text{storage}_{i, 0} = \text{init\_amount}_{i} \quad \forall i \\
  & \text{storage}_{i, M} = \text{init\_amount}_{i} \quad \forall i \\
  & 0 \leq \text{refine}_{i, m} \leq \begin{cases} 
      \text{max\_veg} & \text{if } \text{is\_vegetable}_{i} = 1 \\
      \text{max\_non\_veg} & \text{if } \text{is\_vegetable}_{i} = 0 
    \end{cases} \quad \forall i, m \\
  & 0 \leq \text{storage}_{i, m} \leq \text{storage\_size} \quad \forall i, m \\
  & \text{min\_hardness} \leq \frac{\sum_{i=1}^{I} \text{hardness}_{i} \cdot \text{refine}_{i, m}}{\sum_{i=1}^{I} \text{refine}_{i, m}} \leq \text{max\_hardness} \quad \forall m \\
  & \text{buyquantity}_{i, m}, \text{refine}_{i, m}, \text{storage}_{i, m} \geq 0 \quad \forall i, m
\end{align*}

\subsection*{Notes}
- The objective function captures the profit as the difference between revenue from selling refined oil and the costs of purchasing and storing raw oils.
- The constraints ensure the balance of storage, respect refining capacity per type of oil, impose storage limits, and enforce the hardness requirement on the final product.

\end{document}
```

This model takes into account all specified constraints and aims to maximize the profit by optimizing the decision on quantities to buy, store, and refine each type of raw oil per month.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
Let:
\begin{align*}
  & \text{buyquantity}_{i, m} \quad \text{be the quantity of oil $i$ bought in month $m$.} \\
  & \text{refine}_{i, m} \quad \text{be the quantity of oil $i$ refined in month $m$.} \\
  & \text{storage}_{i, m} \quad \text{be the quantity of oil $i$ stored at the end of month $m$.}
\end{align*}

\subsection*{Objective Function}
Maximize the total profit over the planning horizon:
\begin{align*}
  \text{Maximize} \quad 
  & \sum_{m=1}^{M} \sum_{i=1}^{I} \left[ (\text{sell\_price} \cdot \text{refine}_{i, m}) - (\text{buy\_price}_{i, m} \cdot \text{buyquantity}_{i, m}) - (\text{storage\_cost} \cdot \text{storage}_{i, m}) \right]
\end{align*}

\subsection*{Constraints}
\begin{align*}
  & \text{For each oil } i \text{ and month } m: \\
  & \text{storage}_{i, m} = \text{storage}_{i, m-1} + \text{buyquantity}_{i, m} - \text{refine}_{i, m} \quad \forall i, m \\
  & \text{storage}_{i, 0} = \text{init\_amount}_{i} \quad \forall i \\
  & \text{storage}_{i, M} = \text{init\_amount}_{i} \quad \forall i \\
  & 0 \leq \text{refine}_{i, m} \leq \begin{cases} 
      \text{max\_veg} & \text{if } \text{is\_vegetable}_{i} = 1 \\
      \text{max\_non\_veg} & \text{if } \text{is\_vegetable}_{i} = 0 
    \end{cases} \quad \forall i, m \\
  & 0 \leq \text{storage}_{i, m} \leq \text{storage\_size} \quad \forall i, m \\
  & \text{min\_hardness} \leq \frac{\sum_{i=1}^{I} \text{hardness}_{i} \cdot \text{refine}_{i, m}}{\sum_{i=1}^{I} \text{refine}_{i, m}} \leq \text{max\_hardness} \quad \forall m \\
  & \text{buyquantity}_{i, m}, \text{refine}_{i, m}, \text{storage}_{i, m} \geq 0 \quad \forall i, m
\end{align*}

\subsection*{Notes}
- The objective function captures the profit as the difference between revenue from selling refined oil and the costs of purchasing and storing raw oils.
- The constraints ensure the balance of storage, respect refining capacity per type of oil, impose storage limits, and enforce the hardness requirement on the final product.

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

#### Problem Definition
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

#### Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)

#### Objective Function
profit = pulp.lpSum(
    (data['SellPrice'] * refine[i, m]) -
    (data['BuyPrice'][m][i] * buyquantity[i, m]) -
    (data['StorageCost'] * storage[i, m])
    for i in range(data['I']) for m in range(data['M'])
)

problem += profit

#### Constraints
#### Storage balance
for i in range(data['I']):
    for m in range(1, data['M']):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]
    #### Initial storage
    problem += storage[i, 0] == data['InitialAmount']
    #### Ending storage
    problem += storage[i, data['M'] - 1] == data['InitialAmount']
    
#### Refining capacity constraints
for i in range(data['I']):
    for m in range(data['M']):
        if data['IsVegetable'][i]:
            problem += refine[i, m] <= data['MaxVegetableRefiningPerMonth']
        else:
            problem += refine[i, m] <= data['MaxNonVegetableRefiningPerMonth']

#### Storage limits
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m] <= data['StorageSize']

#### Hardness constraints
for m in range(data['M']):
    total_refine = pulp.lpSum(refine[i, m] for i in range(data['I']))
    weighted_hardness = pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I']))
    problem += data['MinHardness'] * total_refine <= weighted_hardness
    problem += weighted_hardness <= data['MaxHardness'] * total_refine

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

