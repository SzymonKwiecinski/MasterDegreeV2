import pulp
import json

# Load data
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

# Define model
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(data['I']) for m in range(data['M'])), lowBound=0, upBound=data['StorageSize'])

# Objective Function
profit = pulp.lpSum(data['SellPrice'] * refine[i, m] for i in range(data['I']) for m in range(data['M'])) \
         - pulp.lpSum(data['BuyPrice'][m][i] * buyquantity[i, m] for i in range(data['I']) for m in range(data['M'])) \
         - pulp.lpSum(data['StorageCost'] * storage[i, m] for i in range(data['I']) for m in range(data['M']))

problem += profit, "Total Profit"

# Constraints
# Refining Limitations
for m in range(data['M']):
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if data['IsVegetable'][i]) <= data['MaxVegetableRefiningPerMonth'], f"MaxVegetableRefining_{m}"
    problem += pulp.lpSum(refine[i, m] for i in range(data['I']) if not data['IsVegetable'][i]) <= data['MaxNonVegetableRefiningPerMonth'], f"MaxNonVegetableRefining_{m}"

# Storage Dynamics
for i in range(data['I']):
    for m in range(1, data['M']):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m], f"StorageDynamics_{i}_{m}"

    # Initial and final storage amounts
    problem += storage[i, 0] == data['InitialAmount'], f"InitialStorage_{i}"
    problem += storage[i, data['M'] - 1] == data['InitialAmount'], f"FinalStorage_{i}"

# Storage Capacity
for i in range(data['I']):
    for m in range(data['M']):
        problem += storage[i, m] >= 0, f"NonNegativeStorage_{i}_{m}"
        problem += storage[i, m] <= data['StorageSize'], f"StorageCapacity_{i}_{m}"

# Hardness Constraints
for m in range(data['M']):
    total_refine = pulp.lpSum(refine[i, m] for i in range(data['I']))
    problem += total_refine >= 0.001, f"NonZeroRefine_{m}"  # To avoid division by zero
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refine >= data['MinHardness']), f"MinHardness_{m}"
    problem += (pulp.lpSum(data['Hardness'][i] * refine[i, m] for i in range(data['I'])) / total_refine <= data['MaxHardness']), f"MaxHardness_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')