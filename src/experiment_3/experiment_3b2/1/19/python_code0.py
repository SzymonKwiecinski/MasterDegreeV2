import pulp
import json

# Data from JSON
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

# Indices
I = len(data['is_vegetable'])
M = len(data['buy_price'][0])

# Create the LP problem
problem = pulp.LpProblem("Oil_Refining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)
use = pulp.LpVariable.dicts("use", (range(I), range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(data['buy_price'][i][m] * buyquantity[i][m] + data['storage_cost'] * storage[i][m] 
                      for i in range(I) for m in range(M))
problem += profit

# Constraints

# Refinement Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage and Balance Constraints
for i in range(I):
    problem += storage[i][0] == data['init_amount']
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]
    # Last month storage constraint
    problem += storage[i][M-1] == data['init_amount']
    for m in range(M):
        problem += storage[i][m] >= 0
        problem += storage[i][m] <= data['storage_size']

# Hardness Constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) \
               / pulp.lpSum(refine[i][m] for i in range(I)) >= data['min_hardness']
    problem += pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) \
               / pulp.lpSum(refine[i][m] for i in range(I)) <= data['max_hardness']

# Usage Constraints
for m in range(M):
    problem += pulp.lpSum(use[i][m] for i in range(I)) <= 3
    for i in range(I):
        problem += data['min_usage'] * use[i][m] <= refine[i][m]
        problem += refine[i][m] <= storage[i][m-1] + buyquantity[i][m]
        for j in range(I):
            problem += use[i][m] >= use[j][m] * data['dependencies'][i][j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')