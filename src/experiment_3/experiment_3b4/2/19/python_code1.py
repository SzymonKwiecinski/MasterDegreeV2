import pulp

# Data given
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

I = len(data['buy_price'])  # number of items
M = len(data['buy_price'][0])  # number of months

# Create a linear programming problem
problem = pulp.LpProblem("Refinery_Optimization", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("Use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Initial storage amounts
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Objective function
objective = pulp.lpSum([
    data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I)) -
    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + data['storage_cost'] * storage[i, m+1] for i in range(I))
    for m in range(M)
])
problem += objective

# Constraints
for m in range(M):
    for i in range(I):
        # Balance constraint
        problem += storage[i, m+1] == storage[i, m] + buyquantity[i, m] - refine[i, m]

        # Storage capacity constraint
        problem += storage[i, m] <= data['storage_size']

        # Minimum usage constraint
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

        for j in range(I):
            if j < len(data['dependencies'][i]):  # Check if j is a valid index for dependencies
                # Dependency constraint
                problem += use[i, m] >= use[j, m] * data['dependencies'][i][j]

    # Hardness constraints
    total_refine_per_month = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) <= data['max_hardness'] * total_refine_per_month
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) >= data['min_hardness'] * total_refine_per_month

    # Vegetable and non-vegetable refining constraints
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Maximum number of items used constraint
    problem += pulp.lpSum(use[i, m] for i in range(I)) <= 3

# Final storage constraint
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')