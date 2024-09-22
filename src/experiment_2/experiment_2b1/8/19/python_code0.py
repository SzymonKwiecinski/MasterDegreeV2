import pulp
import json

# Input data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Parameters
I = len(data['buy_price'][0])  # number of oils
M = len(data['buy_price'])      # number of months
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
init_amount = data['init_amount']
min_usage = data['min_usage']
hardness = data['hardness']
vegetable_indices = [i for i in range(I) if data['is_vegetable'][i]]
non_vegetable_indices = [i for i in range(I) if not data['is_vegetable'][i]]

# Model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((sell_price * pulp.lpSum(refine[i][m] for i in range(I)) 
                     - data['buy_price'][m][i] * buyquantity[i][m]
                     - data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M)))
problem += profit

# Constraints
for m in range(M):
    # Refining constraints
    problem += pulp.lpSum(refine[i][m] for i in vegetable_indices) <= max_veg, f"MaxVegRefineMonth{m}"
    problem += pulp.lpSum(refine[i][m] for i in non_vegetable_indices) <= max_non_veg, f"MaxNonVegRefineMonth{m}"
    
    # Buy quantity limit
    problem += pulp.lpSum(buyquantity[i][m] for i in range(I)) <= data['storage_size'], f"BuyLimitMonth{m}"
    
    # Dependencies
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[i][m] <= refine[i][m] + refine[j][m], f"DependencyOil{i}_to_{j}_Month{m}"

    # Minimum usage constraint
    for i in range(I):
        problem += refine[i][m] >= min_usage * pulp.lpSum(refine[i][m] > 0), f"MinUsageOil{i}_Month{m}"

# Storage at the end of the month
for m in range(M):
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == init_amount, f"InitialStorageOil{i}_Month0"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m-1] - refine[i][m-1], f"StorageOil{i}_Month{m}"
    
# Storage should be equal to the initial amount at the end of the last month
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"FinalStorageOil{i}"

# Solve the problem
problem.solve()

# Extract results
buy = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_results = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_results = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output results
output = {
    "buy": buy,
    "refine": refine_results,
    "storage": storage_results
}

print(json.dumps(output, indent=4))