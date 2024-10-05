import pulp
import json

# Load data from JSON
data_json = '''{
    "M": 6, 
    "I": 5, 
    "BuyPrice": [
        [110, 120, 130, 110, 115], 
        [130, 130, 110, 90, 115], 
        [110, 140, 130, 100, 95], 
        [120, 110, 120, 120, 125], 
        [100, 120, 150, 110, 105], 
        [90, 100, 140, 80, 135]
    ], 
    "SellPrice": 150, 
    "IsVegetable": [true, true, false, false, false], 
    "MaxVegetableRefiningPerMonth": 200, 
    "MaxNonVegetableRefiningPerMonth": 250, 
    "StorageSize": 1000, 
    "StorageCost": 5, 
    "MinHardness": 3, 
    "MaxHardness": 6, 
    "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], 
    "InitialAmount": 500
}'''

data = json.loads(data_json)

# Prepare problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(data['I']), range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(data['I']), range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(data['I']), range(data['M'])), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['SellPrice'] * pulp.lpSum(refine[i][m] for i in range(data['I'])) for m in range(data['M']))
costs = pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for m in range(data['M']) for i in range(data['I']))
storage_cost = data['StorageCost'] * pulp.lpSum(storage[i][m] for m in range(data['M']) for i in range(data['I']))
problem += profit - costs - storage_cost

# Constraints
# Storage dynamics
for m in range(data['M']):
    for i in range(data['I']):
        if m == 0:
            problem += storage[i][m] == data['InitialAmount'] + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Refining Capacity Constraints
for m in range(data['M']):
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Storage Limit Constraints
for m in range(data['M']):
    for i in range(data['I']):
        problem += storage[i][m] <= data['StorageSize']

# Hardness Constraint
for m in range(data['M']):
    total_refine = pulp.lpSum(refine[i][m] for i in range(data['I']))
    hardness_sum = pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I']))
    problem += total_refine >= 0 
    problem += pulp.lpSum(refine[i][m] for i in range(data['I'])) > 0
    problem += (hardness_sum / total_refine) >= data['MinHardness']
    problem += (hardness_sum / total_refine) <= data['MaxHardness']

# Initial and Final Storage Constraints
for i in range(data['I']):
    problem += storage[i][data['M']-1] == data['InitialAmount']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')