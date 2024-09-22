import pulp
import json

data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95],
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Problem Setup
I = len(data['buy_price'][0])
M = len(data['buy_price'])
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
hardness_min = data['min_hardness']
hardness_max = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Create the LP problem
problem = pulp.LpProblem("Oil_Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function
problem += pulp.lpSum((sell_price * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M))) -
                       pulp.lpSum(buyquantity[i][m] * data['buy_price'][m][i] for i in range(I) for m in range(M)) -
                       pulp.lpSum(storage[i][m] * storage_cost for i in range(I) for m in range(M))), "Total Profit"

# Constraints
# Initial storage
for i in range(I):
    problem += storage[i][0] == init_amount, f"InitialStorageOil_{i}"

# Storage Update
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageUpdateOil_{i}_{m}"

# Ending storage requirement
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"EndingStorageOil_{i}"

# Monthly refining limits
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= max_veg, f"MaxVegRefining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg, f"MaxNonVegRefining_{m}"

# Minimum usage
for i in range(I):
    for m in range(M):
        problem += refine[i][m] >= min_usage * pulp.lpSum(dependencies[i]), f"MinUsageOil_{i}_{m}"

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i][m] for i in range(I))
    if total_refined > 0:
        problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) / total_refined) >= hardness_min, f"MinHardness_{m}"
        problem += (pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) / total_refined) <= hardness_max, f"MaxHardness_{m}"

# Solve the problem
problem.solve()

# Output results
buy_output = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_output,
    "refine": refine_output,
    "storage": storage_output
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')