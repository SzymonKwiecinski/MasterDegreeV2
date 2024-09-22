import pulp

# Data from JSON
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

# Problem
problem = pulp.LpProblem("Oil_Refining", pulp.LpMaximize)

# Parameters
I = len(data['buy_price'])  # Number of oils
M = len(data['buy_price'][0])  # Number of months

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
binary_refine = pulp.LpVariable.dicts("binary_refine", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective function
problem += pulp.lpSum([
    data['sell_price'] * pulp.lpSum([refine[i, m] for i in range(I)]) -
    pulp.lpSum([data['buy_price'][i][m] * buyquantity[i, m] for i in range(I)]) -
    pulp.lpSum([data['storage_cost'] * storage[i, m] for i in range(I)])
    for m in range(M)
])

# Constraints
for i in range(I):
    # Initial storage
    problem += storage[i, 0] == data['init_amount'], f"InitialStorage_{i}"

    # Final storage
    problem += storage[i, M] == data['init_amount'], f"FinalStorage_{i}"

    for m in range(1, M + 1):
        # Storage Balance
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m - 1] - refine[i, m - 1], f"StorageBalance_{i}_{m}"

        # Storage Capacity
        problem += storage[i, m] <= data['storage_size'], f"StorageCapacity_{i}_{m}"

for m in range(M):
    # Refining Capacity
    problem += pulp.lpSum([refine[i, m] for i in range(I) if data['is_vegetable'][i]]) <= data['max_vegetable_refining_per_month'], f"VegCapacity_{m}"
    problem += pulp.lpSum([refine[i, m] for i in range(I) if not data['is_vegetable'][i]]) <= data['max_non_vegetable_refining_per_month'], f"NonVegCapacity_{m}"

    # Hardness Constraint
    total_refine = pulp.lpSum([refine[i, m] for i in range(I)])
    problem += (
        pulp.lpSum([data['hardness'][i] * refine[i, m] for i in range(I)]) >= data['min_hardness'] * total_refine,
        f"MinHardness_{m}"
    )
    problem += (
        pulp.lpSum([data['hardness'][i] * refine[i, m] for i in range(I)]) <= data['max_hardness'] * total_refine,
        f"MaxHardness_{m}"
    )

    # Oil Usage Limit
    problem += pulp.lpSum([binary_refine[i, m] for i in range(I)]) <= 3, f"OilUsageLimit_{m}"

    # Minimum Usage
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * binary_refine[i, m], f"MinUsage_{i}_{m}"
        
    # Dependency Constraints
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[j, m] >= refine[i, m], f"Dependency_{i}_{j}_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')