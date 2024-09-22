import pulp

# Parse the input data
data = {
    'num_machines': [4, 2, 3, 1, 1], 
    'profit': [10, 6, 8, 4, 11, 9, 3], 
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
             [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], 
             [0.5, 0.0, 0.6, 0.08, 0.05]], 
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

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

K = len(profit)
M = len(num_machines)
I = len(limit[0])
max_storage = 100
work_days = 24
shifts_per_day = 2

# Total available work hours
total_work_hours = work_days * shifts_per_day * n_workhours

# Set up the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        problem += sell[k, i] <= limit[k][i], f"Sell_Limit_{k}_{i}"
        if i == 0:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i], f"Initial_Storage_Balance_{k}_{i}"
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i], f"Storage_Balance_{k}_{i}"
    
    for m in range(M):
        machine_hours_available = num_machines[m] * total_work_hours - down[m] * total_work_hours
        problem += pulp.lpSum(manufacture[k, i] * time[k][m] for k in range(K)) <= machine_hours_available, f"Machine_Time_{m}_{i}"

# Maintain constraints
for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m], f"Maintenance_Schedule_{m}"
    for i in range(I):
        problem += maintain[m, i] >= 0, f"Non_Negative_Maintenance_{m}_{i}"

# Closing stock constraints
for k in range(K):
    problem += storage[k, I-1] == keep_quantity, f"Closing_Stock_{k}"

# Solve the problem
problem.solve()

# Output results
output = {
    "sell": [[pulp.value(sell[k, i]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[k, i]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[k, i]) for k in range(K)] for i in range(I)],
    "maintain": [[pulp.value(maintain[m, i]) for m in range(M)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')