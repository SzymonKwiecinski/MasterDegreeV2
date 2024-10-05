import pulp

# Parsing the data
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
    'down': [0, 1, 1, 1, 1],
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

num_m = len(data['num_machines'])
num_k = len(data['profit'])
num_i = len(data['limit'][0])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", (range(num_i), range(num_k)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", (range(num_i), range(num_k)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(num_i), range(num_k)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", (range(num_i), range(num_m)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[i][k] for i in range(num_i) for k in range(num_k)) - \
            pulp.lpSum(data['store_price'] * storage[i][k] for i in range(num_i) for k in range(num_k))

# Constraints
for i in range(num_i):
    for k in range(num_k):
        if i == 0:
            problem += manufacture[i][k] == sell[i][k] + storage[i][k]
        else:
            problem += manufacture[i][k] + storage[i-1][k] == sell[i][k] + storage[i][k]
        problem += sell[i][k] <= data['limit'][k][i]

    for m in range(num_m):
        problem += maintain[i][m] >= data['down'][m]
        problem += maintain[i][m] <= data['num_machines'][m]

    for k in range(num_k):
        hourly_capacity = 24 * 6 * 2 * data['n_workhours']
        # Production time constraint
        problem += pulp.lpSum(data['time'][k][m] * manufacture[i][k] for m in range(num_m)) <= \
                   hourly_capacity - pulp.lpSum(maintain[i][m] * data['time'][k][m] for m in range(num_m))

# Final month stocks
for k in range(num_k):
    problem += storage[num_i-1][k] == data['keep_quantity']

# Solve the problem
problem.solve()

# Output
output = {
    "sell": [[pulp.value(sell[i][k]) for k in range(num_k)] for i in range(num_i)],
    "manufacture": [[pulp.value(manufacture[i][k]) for k in range(num_k)] for i in range(num_i)],
    "storage": [[pulp.value(storage[i][k]) for k in range(num_k)] for i in range(num_i)],
    "maintain": [[pulp.value(maintain[i][m]) for m in range(num_m)] for i in range(num_i)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')