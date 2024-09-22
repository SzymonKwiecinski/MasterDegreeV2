import pulp
import json

# Load data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Fix boolean values
data['is_vegetable'] = [bool(v) for v in data['is_vegetable']]

# Define the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Sets and indices
I = range(len(data['buy_price']))  # Set of oils
M = range(len(data['buy_price'][0]))  # Set of months

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (I, M), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (I, M), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (I, M), lowBound=0, upBound=data['storage_size'], cat='Continuous')
use = pulp.LpVariable.dicts("use", (I, M), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] for i in I for m in M) \
         - pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] for i in I for m in M) \
         - pulp.lpSum(data['storage_cost'] * storage[i][m] for i in I for m in M)

problem += profit

# Constraints

# Inventory Balance
for i in I:
    problem += storage[i][0] == data['init_amount']
    for m in range(1, len(M)):
        problem += storage[i][m-1] + buyquantity[i][m] - refine[i][m] == storage[i][m]

# Refining Capacity
for m in M:
    problem += pulp.lpSum(refine[i][m] for i in I if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in I if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Limits
for i in I:
    for m in M:
        problem += storage[i][m] >= 0
        problem += storage[i][m] <= data['storage_size']

# Hardness Constraints
for m in M:
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in I) / pulp.lpSum(refine[i][m] for i in I) >= data['min_hardness']
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in I) / pulp.lpSum(refine[i][m] for i in I) <= data['max_hardness']

# Final Storage Requirement
for i in I:
    problem += storage[i][len(M)-1] == data['init_amount']

# Usage Constraints
for m in M:
    for i in I:
        problem += refine[i][m] >= data['min_usage'] * use[i][m]
    problem += pulp.lpSum(use[i][m] for i in I) <= 3

# Dependency Constraints
for m in M:
    for i in I:
        for j in I:
            if data['dependencies'][i][j] == 1:
                problem += use[i][m] <= use[j][m] + 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')