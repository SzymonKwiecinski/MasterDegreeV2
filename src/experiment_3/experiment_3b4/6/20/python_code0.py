import pulp

# Data from the JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Problem variables
K = len(data['profit'])  # number of products
I = len(data['limit'][0])  # number of months
M = len(data['num_machines'])  # number of machines

# Create the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i]
                         for k in range(K) for i in range(I))
problem += profit_expr, "Total Profit"

# Constraints

# 1. Production Constraints
for i in range(I):
    for k in range(K):
        problem += (pulp.lpSum(data['time'][k][m] * manufacture[k, i] for m in range(M)) <=
                    pulp.lpSum((data['num_machines'][m] - data['maintain'][m][i]) * 24 * data['n_workhours']
                               for m in range(M))), f"Production_Constraint_{k}_{i}"

# 2. Demand/Sales Constraints
for i in range(I):
    for k in range(K):
        problem += (sell[k, i] <= data['limit'][k][i]), f"Sales_Limit_{k}_{i}"

# 3. Storage Balance Constraints
for i in range(I):
    for k in range(K):
        if i == 0:
            problem += (manufacture[k, i] == sell[k, i] + storage[k, i]), f"Storage_Balance_Init_{k}_{i}"
        else:
            problem += (storage[k, i - 1] + manufacture[k, i] == sell[k, i] + storage[k, i]), f"Storage_Balance_{k}_{i}"

# 4. Storage Capacity Constraints
for i in range(I):
    for k in range(K):
        problem += (storage[k, i] <= 100), f"Storage_Capacity_{k}_{i}"

# 5. End of Period Stock Constraints
for k in range(K):
    problem += (storage[k, I - 1] >= data['keep_quantity']), f"End_Period_Stock_{k}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')