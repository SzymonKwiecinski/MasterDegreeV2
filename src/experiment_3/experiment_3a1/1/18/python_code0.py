import pulp
import json

# Data input
data_json = '''{
    "M": 6,
    "I": 5,
    "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(data['I']), range(data['M'])), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(data['I']), range(data['M'])), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(data['I']), range(data['M'] + 1)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['SellPrice'] * refine[i][m] for i in range(data['I']) for m in range(data['M'])) - \
         pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(data['I']) for m in range(data['M'])) - \
         pulp.lpSum(data['StorageCost'] * storage[i][m] for i in range(data['I']) for m in range(data['M']))

problem += profit

# Constraints

# Storage Dynamics
for i in range(data['I']):
    for m in range(1, data['M']):
        problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m]
    problem += storage[i][0] == data['InitialAmount']
    problem += storage[i][data['M']] == data['InitialAmount']
    problem += storage[i][m] <= data['StorageSize']

# Refining Capacity
for m in range(data['M']):
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth']
    problem += pulp.lpSum(refine[i][m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth']

# Hardness Restrictions
for m in range(data['M']):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) /
                pulp.lpSum(refine[i][m] for i in range(data['I'])) >= data['MinHardness']) if pulp.lpSum(refine[i][m] for i in range(data['I'])) > 0 else 0
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i][m] for i in range(data['I'])) /
                pulp.lpSum(refine[i][m] for i in range(data['I'])) <= data['MaxHardness']) if pulp.lpSum(refine[i][m] for i in range(data['I'])) > 0 else 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')