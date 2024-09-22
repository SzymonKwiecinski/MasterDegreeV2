import pulp
import json

# Data from JSON format
data = json.loads('{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}')

# Constants
I = len(data['buy_price'])  # number of different oils
M = len(data['buy_price'][0])  # number of months

# Problem Definition
problem = pulp.LpProblem("Oil_Refining_Optimization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['sell_price'] * refine[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] for i in range(I) for m in range(M)) - \
         pulp.lpSum(data['storage_cost'] * storage[i, m] for i in range(I) for m in range(M))

problem += profit, "Total_Profit"

# Constraints

# 1. Storage dynamics
for i in range(I):
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m - 1] + buyquantity[i, m] - refine[i, m], f"Storage_Dynamics_{i}_{m}"

# 2. Initial storage
for i in range(I):
    problem += storage[i, 0] == data['init_amount'], f"Initial_Storage_{i}"

# 3. Final storage requirement
for i in range(I):
    problem += storage[i, M - 1] == data['init_amount'], f"Final_Storage_{i}"

# 4. Maximum refining capacity (vegetable)
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"Max_Veg_Refining_{m}"

# 5. Maximum refining capacity (non-vegetable)
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"Max_Non_Veg_Refining_{m}"

# 6. Hardness constraints
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in range(I)), f"Min_Hardness_{m}"
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in range(I)), f"Max_Hardness_{m}"

# 7. Min usage constraint
usage = pulp.LpVariable.dicts("use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')
for i in range(I):
    for m in range(M):
        problem += refine[i, m] >= data['min_usage'] * usage[i, m], f"Min_Usage_{i}_{m}"

# 8. Dependency constraints
for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += refine[i, m] <= storage[i, m - 1] + buyquantity[i, m], f"Dependency_{i}_{j}_{m}"

# 9. At most three oils used
for m in range(M):
    problem += pulp.lpSum(usage[i, m] for i in range(I)) <= 3, f"Max_Three_Oils_{m}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')