# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
    'BuyPrice': [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135]
    ],
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

#### Unpack data
I = data['I']
M = data['M']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining_per_month = data['MaxVegetableRefiningPerMonth']
max_non_vegetable_refining_per_month = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

#### Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", [(i, m) for i in range(I) for m in range(M)], lowBound=0, cat='Continuous')
refine_quantity = pulp.LpVariable.dicts("RefineQuantity", [(i, m) for i in range(I) for m in range(M)], lowBound=0, cat='Continuous')
storage_quantity = pulp.LpVariable.dicts("StorageQuantity", [(i, m) for i in range(I) for m in range(M+1)], lowBound=0, cat='Continuous')

#### Add initial storage amount
for i in range(I):
    problem += storage_quantity[i, 0] == initial_amount

#### Constraints
for m in range(M):
    #### Refining capacity constraints
    problem += pulp.lpSum(refine_quantity[i, m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine_quantity[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month
    
    #### Storage constraints
    for i in range(I):
        problem += storage_quantity[i, m+1] == storage_quantity[i, m] + buy_quantity[i, m] - refine_quantity[i, m]
        problem += storage_quantity[i, m+1] <= storage_size
    
    #### Hardness constraints
    total_refine = pulp.lpSum(refine_quantity[i, m] for i in range(I))
    problem += pulp.lpSum(hardness[i] * refine_quantity[i, m] for i in range(I)) >= min_hardness * total_refine
    problem += pulp.lpSum(hardness[i] * refine_quantity[i, m] for i in range(I)) <= max_hardness * total_refine

#### Final storage must equal initial amount
for i in range(I):
    problem += storage_quantity[i, M] == initial_amount

#### Objective
profit = pulp.lpSum(
    sell_price * pulp.lpSum(refine_quantity[i, m] for i in range(I)) 
    - pulp.lpSum(buy_price[m][i] * buy_quantity[i, m] for i in range(I))
    - storage_cost * pulp.lpSum(storage_quantity[i, m+1] for i in range(I))
    for m in range(M)
)
problem += profit

#### Solve
problem.solve()

#### Output
buy_solution = [[pulp.value(buy_quantity[i, m]) for i in range(I)] for m in range(M)]
refine_solution = [[pulp.value(refine_quantity[i, m]) for i in range(I)] for m in range(M)]
storage_solution = [[pulp.value(storage_quantity[i, m]) for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_solution,
    "refine": refine_solution,
    "storage": storage_solution
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

