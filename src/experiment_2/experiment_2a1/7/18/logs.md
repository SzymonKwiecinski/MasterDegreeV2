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
import json
import pulp

#### Input data
data = {
    'M': 6,
    'I': 5,
    'BuyPrice': [[110, 120, 130, 110, 115], 
                 [130, 130, 110, 90, 115], 
                 [110, 140, 130, 100, 95], 
                 [120, 110, 120, 120, 125], 
                 [100, 120, 150, 110, 105], 
                 [90, 100, 140, 80, 135]],
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

#### Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Variable definitions
M = data['M']
I = data['I']
buyquantity = pulp.LpVariable.dicts("BuyQuantity", (range(I), range(M)), 0)
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), 0)
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M)), 0)

#### Objective function
profit = pulp.lpSum([(data['SellPrice'] * pulp.lpSum(refine[i][m] for i in range(I))) -
                      pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(I)))
                     for m in range(M)])

problem += profit

#### Constraints

#### Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"MaxVegetableRefining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegetableRefining_{m}"

#### Storage capacity constraints
for m in range(M):
    for i in range(I):
        problem += storage[i][m] <= data['StorageSize'], f"StorageCapacity_{i}_{m}"

#### Initial storage
for i in range(I):
    problem += storage[i][0] == data['InitialAmount'], f"InitialStorage_{i}"

#### Storage balance constraints
for m in range(M-1):
    for i in range(I):
        problem += storage[i][m] + buyquantity[i][m] - refine[i][m] == storage[i][m+1], f"StorageBalance_{i}_{m}"

#### Final storage must equal initial storage
for i in range(I):
    problem += storage[i][M-1] == data['InitialAmount'], f"FinalStorage_{i}"

#### Hardness constraints
problem += pulp.lpSum(data['Hardness'][i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) <= data['MaxHardness'], "MaxHardness"
problem += pulp.lpSum(data['Hardness'][i] * pulp.lpSum(refine[i][m] for m in range(M)) for i in range(I)) / pulp.lpSum(refine[i][m] for i in range(I)) >= data['MinHardness'], "MinHardness"

#### Solve the problem
problem.solve()

#### Prepare output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

#### Print results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

