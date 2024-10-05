from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
import json

# Parse the input data
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

# Initialize the problem
problem = LpProblem("Oil_Production_Optimization", LpMaximize)

# Decision variables
buy = LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)

# Objective function: maximize the profit
problem += lpSum(
    sell_price * lpSum(refine[i, m] for i in range(I)) -
    lpSum(buy[i, m] * buy_price[m][i] for i in range(I)) -
    lpSum(storage[i, m] * storage_cost for i in range(I))
    for m in range(M)
)

# Initial storage constraints
for i in range(I):
    problem += storage[i, 0] == init_amount

# Storage balance and refining constraints
for m in range(M):
    for i in range(I):
        problem += storage[i, m + 1] == storage[i, m] + buy[i, m] - refine[i, m]

for m in range(M):
    problem += lpSum(refine[i, m] for i in range(I) if is_vegetable[i]) <= max_veg
    problem += lpSum(refine[i, m] for i in range(I) if not is_vegetable[i]) <= max_non_veg

    # Hardness constraint
    problem += lpSum(refine[i, m] * hardness[i] for i in range(I)) >= min_hardness * lpSum(refine[i, m] for i in range(I))
    problem += lpSum(refine[i, m] * hardness[i] for i in range(I)) <= max_hardness * lpSum(refine[i, m] for i in range(I))

# Storage size constraints
for i in range(I):
    for m in range(1, M + 1):
        problem += storage[i, m] <= storage_size

# Ensure storage returns to initial amount
for i in range(I):
    problem += storage[i, M] == init_amount

# Solve the problem
problem.solve()

# Prepare the results
buy_result = [[value(buy[i, m]) for i in range(I)] for m in range(M)]
refine_result = [[value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_result = [[value(storage[i, m]) for i in range(I)] for m in range(M + 1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result[:-1]  # Exclude the storage at month M+1
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')