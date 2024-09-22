import pulp
import json

# Data provided in JSON format
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

# Create a linear programming problem
problem = pulp.LpProblem("Oil_Management_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(data['M'])) - \
           pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i, m] for i in range(data['I']) for m in range(data['M'])) - \
           data['StorageCost'] * pulp.lpSum(storage[i, m] for i in range(data['I']) for m in range(data['M']))

# Constraints
for m in range(data['M']):
    for i in range(data['I']):
        if m == 0:  # Initial storage
            problem += storage[i, m] == data['InitialAmount'] + buyquantity[i, m] - refine[i, m], f"Balance_Storage_{i}_{m}"
        else:  # Balance Constraint for Storage
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m], f"Balance_Storage_{i}_{m}"
    
    # Refining Capacity Constraints
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"MaxVegRefine_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegRefine_{m}"
    
    # Storage Capacity Constraints
    for i in range(data['I']):
        problem += storage[i, m] <= data['StorageSize'], f"Storage_Capacity_{i}_{m}"

    # Hardness Constraints
    total_refine = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refine >= data['MinHardness']), f"Min_Hardness_{m}"
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refine <= data['MaxHardness']), f"Max_Hardness_{m}"

# Final storage constraints
for i in range(data['I']):
    problem += storage[i, data['M'] - 1] == data['InitialAmount'], f"Final_Storage_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')