import pulp

# Extracting data from the provided JSON
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

I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Creating the optimization problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective function
problem += pulp.lpSum((data['sell_price'] * refine[i, m] 
                       - data['buy_price'][i][m] * buy[i, m] 
                       - data['storage_cost'] * storage[i, m]) for i in range(I) for m in range(M))

# Initial storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Flow balance constraints
for i in range(I):
    for m in range(1, M + 1):
        problem += storage[i, m] == storage[i, m - 1] + buy[i, m - 1] - refine[i, m - 1]

# Storage capacity constraints
for i in range(I):
    for m in range(M + 1):  # fixed: changed M to M + 1 to include the last month
        problem += storage[i, m] <= data['storage_size']

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))

# Usage limitations
for m in range(M):
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

# Minimum usage constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

# Dependency constraints
for i in range(I):
    for j in range(I):
        for m in range(M):
            problem += use[i, m] <= use[j, m] + (1 - data['dependencies'][i][j])

# Final storage requirement
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')