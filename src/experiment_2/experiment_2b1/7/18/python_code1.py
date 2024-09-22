import pulp
import json

# Input data
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

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
M = data['M']
I = data['I']

buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((data['SellPrice'] * pulp.lpSum(refine[i][m] for i in range(I)) 
                     - pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i][m] for i in range(I)) 
                     - data['StorageCost'] * pulp.lpSum(storage[i][m] for i in range(I))) 
                     for m in range(M))

problem += profit

# Constraints
for m in range(M):
    # Refining capacity constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"MaxVegRefine_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegRefine_{m}"
    
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == data['InitialAmount'], f"InitialStorage_{i}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m-1] - refine[i][m-1], f"StorageBalance_{i}_{m}"

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i][m] for i in range(I))
    hardness_expr = pulp.lpSum(data['Hardness'][i] * (refine[i][m] / total_refined) 
                                for i in range(I) if total_refined > 0)
    problem += hardness_expr >= data['MinHardness'], f"MinHardness_{m}"
    problem += hardness_expr <= data['MaxHardness'], f"MaxHardness_{m}"

# Final storage constraint
for i in range(I):
    problem += storage[i][M-1] == data['InitialAmount'], f"FinalStorage_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
            "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
            "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
print(json.dumps(output))