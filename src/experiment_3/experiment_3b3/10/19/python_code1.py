import pulp

# Data
data = {
    'buy_price': [
        [110, 120, 130, 110, 115],
        [130, 130, 110, 90, 115],
        [110, 140, 130, 100, 95],
        [120, 110, 120, 120, 125],
        [100, 120, 150, 110, 105],
        [90, 100, 140, 80, 135]
    ],
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
    'dependencies': [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
}

I = len(data['buy_price'])
M = len(data['buy_price'][0])

# Define indices for oils and months
oil_types = range(I)
months = range(1, M + 1)

# Create the LP problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", [(i, m) for i in oil_types for m in months], lowBound=0)
refine = pulp.LpVariable.dicts("refine", [(i, m) for i in oil_types for m in months], lowBound=0)
storage = pulp.LpVariable.dicts("storage", [(i, m) for i in oil_types for m in range(M + 1)], lowBound=0)
y = pulp.LpVariable.dicts("y", [(i, m) for i in oil_types for m in months], cat='Binary')

# Objective Function
problem += pulp.lpSum([
    data['sell_price'] * refine[i, m] - 
    buyquantity[i, m] * data['buy_price'][i][m-1] - 
    data['storage_cost'] * storage[i, m] 
    for i in oil_types 
    for m in months
])

# Constraints
for i in oil_types:
    # Initial Storage
    problem += storage[i, 0] == data['init_amount']

    # Final Storage Requirement
    problem += storage[i, M] == data['init_amount']

    for m in months:
        # Storage Balance
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]

# Refining Capacity
for m in months:
    problem += pulp.lpSum(refine[i, m] for i in oil_types if i < len(data['is_vegetable']) and data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in oil_types if i < len(data['is_vegetable']) and not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraints
for m in months:
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in oil_types) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in oil_types)
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in oil_types) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in oil_types)

# Oil Usage Constraints
for i in oil_types:
    for m in months:
        problem += refine[i, m] >= data['min_usage'] * y[i, m]

for m in months:
    problem += pulp.lpSum(y[i, m] for i in oil_types) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')