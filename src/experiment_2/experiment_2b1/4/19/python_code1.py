import json
import pulp

# Load the data from the input format
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
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
}

# Problem Data
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])  # Number of months

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buy_quantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([
    data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I)) -
    pulp.lpSum(data['buy_price'][m][i] * buy_quantity[i][m] for i in range(I)) -
    data['storage_cost'] * pulp.lpSum(storage[i][m] for i in range(I)) 
    for m in range(M)
])
problem += profit

# Constraints
for m in range(M):
    # Storage constraints
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == data['init_amount'], f"InitStorage_{i}_{m}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buy_quantity[i][m-1] - refine[i][m-1], f"Storage_{i}_{m}"

    # Refining capacity constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"MaxVegRefining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"MaxNonVegRefining_{m}"

    # Hardness constraints
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) /
                 pulp.lpSum(refine[i][m] for i in range(I)) >= data['min_hardness']), f"MinHardness_{m}"
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) /
                 pulp.lpSum(refine[i][m] for i in range(I)) <= data['max_hardness']), f"MaxHardness_{m}"

    # Minimum usage constraints
    for i in range(I):
        if data['dependencies'][i].count(1) > 0:  # If there are dependencies
            for j in range(I):
                if data['dependencies'][i][j] == 1:
                    problem += refine[j][m] >= data['min_usage'] * pulp.lpSum(refine[i][m] > 0), f"MinUsage_{i}_{j}_{m}"

# Final storage constraint
for i in range(I):
    problem += storage[i][M-1] == data['init_amount'], f"FinalStorage_{i}"

# Solve the problem
problem.solve()

# Collect results
result_buy = [[pulp.value(buy_quantity[i][m]) for i in range(I)] for m in range(M)]
result_refine = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
result_storage = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

# Output results
output = {
    "buy": result_buy,
    "refine": result_refine,
    "storage": result_storage
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')