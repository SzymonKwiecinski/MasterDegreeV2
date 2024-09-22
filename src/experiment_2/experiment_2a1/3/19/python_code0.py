import pulp
import json

# Input data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])       # Number of months
init_amount = data['init_amount']
sell_price = data['sell_price']
storage_cost = data['storage_cost']
min_usage = data['min_usage']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([(sell_price * (refine[i][m])) - (data['buy_price'][m][i] * buyquantity[i][m]) - (storage_cost * storage[i][m]) for i in range(I) for m in range(M)])
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        # Storage constraints
        if m == 0:
            problem += storage[i][m] == init_amount, f"Initial_Storage_{i}_{m}"
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Balance_{i}_{m}"

        # Refining constraints
        if data['is_vegetable'][i]:
            problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Max_Vegetable_Refining_{m}"
        else:
            problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"Max_Non_Vegetable_Refining_{m}"

    # Hardness constraints
    problem += pulp.lpSum((data['hardness'][i] * refine[i][m] for i in range(I))) / (pulp.lpSum(refine[i][m] for i in range(I))) <= max_hardness, f"Hardness_Upper_{m}"
    problem += pulp.lpSum((data['hardness'][i] * refine[i][m] for i in range(I))) / (pulp.lpSum(refine[i][m] for i in range(I))) >= min_hardness, f"Hardness_Lower_{m}"

for i in range(I):
    # Dependency constraints
    for j in range(I):
        if data['dependencies'][i][j]:
            for m in range(M):
                problem += refine[i][m] <= (refine[j][m] + (1 - data['dependencies'][i][j]) * 1e6), f"Dependency_{i}_{j}_{m}"

# Minimum usage constraints
for m in range(M):
    for i in range(I):
        problem += refine[i][m] >= min_usage if pulp.lpSum(refine[i][m] for i in range(I)) > 0 else 0, f"Min_Usage_{i}_{m}"

# Final month storage constraint
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"Final_Storage_{i}"

# Solve the problem
problem.solve()

# Collecting results
buy_results = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_results = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_results = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

# Output
output = {
    "buy": buy_results,
    "refine": refine_results,
    "storage": storage_results
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')