import pulp
import numpy as np

# Data from the provided JSON
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

months = len(data['buy_price'][0])  # 5 months
oils = len(data['buy_price'])  # 6 oils

# Initialize the problem
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(oils) for m in range(months)), cat='Binary')

# Objective Function
problem += pulp.lpSum([
    data['sell_price'] * pulp.lpSum([refine[i, m] for i in range(oils)]) -
    pulp.lpSum([data['buy_price'][i][m] * buyquantity[i, m] for i in range(oils)]) -
    data['storage_cost'] * pulp.lpSum([storage[i, m] for i in range(oils)])
    for m in range(months)
])

# Constraints

# Initial storage setup
for i in range(oils):
    storage[i, 0].setInitialValue(data['init_amount'])

# Monthly constraints
for m in range(months):
    # Vegetable and non-vegetable refining constraints
    problem += pulp.lpSum([refine[i, m] * data['is_vegetable'][i] for i in range(oils)]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum([refine[i, m] * (1 - data['is_vegetable'][i]) for i in range(oils)]) <= data['max_non_vegetable_refining_per_month']
    problem += pulp.lpSum([use[i, m] for i in range(oils)]) <= 3  # At most 3 different oils can be used

    # Hardness constraint
    total_refined = pulp.lpSum([refine[i, m] for i in range(oils)])
    if total_refined > 0:
        problem += pulp.lpSum([refine[i, m] * data['hardness'][i] for i in range(oils)]) / total_refined >= data['min_hardness']
        problem += pulp.lpSum([refine[i, m] * data['hardness'][i] for i in range(oils)]) / total_refined <= data['max_hardness']

    # End-of-month storage capacity
    for i in range(oils):
        problem += storage[i, m] <= data['storage_size']

# Inter-month storage constraints and usage constraints
for i in range(oils):
    for m in range(1, months):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m]
        problem += refine[i, m] >= data['min_usage'] * use[i, m]

        # Dependency constraints
        for j in range(oils):
            if data['dependencies'][i][j] == 1:
                problem += refine[i, m] >= refine[j, m]

# Ensure initial and final storage is the same
for i in range(oils):
    problem += storage[i, months - 1] == data['init_amount']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')