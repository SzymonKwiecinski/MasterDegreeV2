import pulp

# Data from JSON format
data = {'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
                 [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
                 [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 
        'maintain': [[1, 0, 0, 0, 1], [0, 0, 0, 1, 1], 
                     [0, 2, 0, 0, 0], [0, 0, 1, 0, 0], 
                     [0, 0, 0, 0, 0]], 
        'limit': [[500, 600, 300, 200, 0], [1000, 500, 600, 300, 100], 
                  [300, 200, 0, 400, 500], [300, 0, 0, 500, 100], 
                  [800, 400, 500, 200, 1000], [200, 300, 400, 0, 300], 
                  [100, 150, 100, 100, 0]], 
        'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}

# Extracting data
num_machines = data["num_machines"]
profit = data["profit"]
time = data["time"]
maintain = data["maintain"]
limit = data["limit"]
store_price = data["store_price"]
keep_quantity = data["keep_quantity"]
n_workhours = data["n_workhours"]

# Derived dimensions
K = len(profit)  # number of products
I = len(limit[0])  # number of months
M = len(num_machines)  # number of machines

# Total working hours available per month
hours_per_month = 24 * 6 * n_workhours

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints

# Manufacturing and storage balance constraints
for k in range(K):
    # Initial storage is zero
    problem += storage[k, 0] == manufacture[k, 0] - sell[k, 0]

    # Subsequent months
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# Maintenance and working hours constraints
for i in range(I):
    for m in range(M):
        available_machines = num_machines[m] - maintain[i][m]
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= available_machines * hours_per_month

# Marketing limitations
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[k][i]

# Final stock requirement
for k in range(K):
    problem += storage[k, I-1] >= keep_quantity

# Solve the problem
problem.solve()

# Preparing output format
sell_result = [[pulp.value(sell[k, i]) for i in range(I)] for k in range(K)]
manufacture_result = [[pulp.value(manufacture[k, i]) for i in range(I)] for k in range(K)]
storage_result = [[pulp.value(storage[k, i]) for i in range(I)] for k in range(K)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')