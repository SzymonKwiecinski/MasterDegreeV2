import pulp

# Data from the problem
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
        [1, 0, 0, 0, 1], 
        [0, 0, 0, 1, 1], 
        [0, 2, 0, 0, 0], 
        [0, 0, 1, 0, 0], 
        [0, 0, 0, 0, 0]
    ], 
    'limit': [
        [500, 600, 300, 200, 0], 
        [1000, 500, 600, 300, 100], 
        [300, 200, 0, 400, 500], 
        [300, 0, 0, 500, 100], 
        [800, 400, 500, 200, 1000], 
        [200, 300, 400, 0, 300], 
        [100, 150, 100, 100, 0]
    ], 
    'store_price': 0.5, 
    'keep_quantity': 100, 
    'n_workhours': 8.0
}

# Variables for the problem dimensions
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines
I = len(data['maintain'])  # Number of months

# Initialize the problem
problem = pulp.LpProblem("Maximize_Factory_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat=pulp.LpContinuous)
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat=pulp.LpContinuous)
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I+1)), lowBound=0, cat=pulp.LpContinuous) # Storage for month I+1 for final keeping stock

# Objective function
profit_gain = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I))
storage_cost = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))
problem += profit_gain - storage_cost

# Constraints
# Initial Storage - no initial stock
for k in range(K):
    problem += storage[k][0] == 0

# Storage balance constraints
for k in range(K):
    for i in range(I):
        problem += manufacture[k][i] + (storage[k][i] if i == 0 else storage[k][i]) == sell[k][i] + storage[k][i+1]

# Marketing limitations
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]

# Machine time constraints
total_available_hours = 24 * data['n_workhours']  # 24 days * 8 hours/day
for i in range(I):
    for m in range(M):
        available_machines = data['num_machines'][m] - data['maintain'][i][m]
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K)) <= available_machines * total_available_hours

# Storage capacity and end-of-period requirements
for k in range(K):
    for i in range(I):
        problem += storage[k][i+1] <= 100
    # End of planning horizon storage
    problem += storage[k][I] == data['keep_quantity']

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k][i]) for k in range(K)] for i in range(I+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')