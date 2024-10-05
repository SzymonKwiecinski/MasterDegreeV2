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

I = len(data['is_vegetable'])  # Correct number of oils based on is_vegetable
M = len(data['buy_price'][0])  # Number of months

# Initialize problem
problem = pulp.LpProblem("FoodManufacturingOptimization", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", (i for i in range(I)), cat='Binary')

# Objective Function
problem += (
    pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) -
    pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))
)

# Constraints
# Initial and Terminal Storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

# Flow Balance
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1]

# Storage Capacity
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= data['storage_size']

# Refining Constraints
V = [i for i in range(I) if data['is_vegetable'][i]]
NV = [i for i in range(I) if not data['is_vegetable'][i]]

for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in V) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in NV) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) <= data['max_hardness'] * total_refined
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) >= data['min_hardness'] * total_refined

# Usage Constraints
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * use[i]

problem += pulp.lpSum(use[i] for i in range(I)) <= 3

# Dependency Constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            problem += use[i] - use[j] <= 0

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')