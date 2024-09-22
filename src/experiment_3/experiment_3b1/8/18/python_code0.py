import pulp
import json

# Data from the provided JSON format
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

# Initialize the LP problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Variables
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

# Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(1, data['M'] + 1)) - \
            pulp.lpSum(data['BuyPrice'][m-1][i] * buyquantity[i, m] + data['StorageCost'] * storage[i, m] 
                       for i in range(data['I']) for m in range(1, data['M'] + 1)), "Total_Profit"

# Constraints
for m in range(1, data['M'] + 1):
    # Refining Capacities
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], "MaxVeg_Refining_%d" % m
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], "MaxNonVeg_Refining_%d" % m

    # Storage Constraints
    for i in range(data['I']):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], "StorageBalance_%d_%d" % (i, m)
        problem += storage[i, m] >= 0, "NonNegativeStorage_%d_%d" % (i, m)
        problem += storage[i, m] <= data['StorageSize'], "StorageLimit_%d_%d" % (i, m)

# Initial and Final Storage
for i in range(data['I']):
    problem += storage[i, 0] == data['InitialAmount'], "InitialStorage_%d" % i
    problem += storage[i, data['M']] == data['InitialAmount'], "FinalStorage_%d" % i

# Hardness Constraints
for m in range(1, data['M'] + 1):
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) >= data['MinHardness']), "MinHardness_%d" % m
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / 
                 pulp.lpSum(refine[i, m] for i in range(data['I'])) <= data['MaxHardness']), "MaxHardness_%d" % m

# Solve the problem
problem.solve()

# Output the results
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