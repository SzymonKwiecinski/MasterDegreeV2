import pulp

# Data
data = {'num_machines': [4, 2, 3, 1, 1], 
        'profit': [10, 6, 8, 4, 11, 9, 3], 
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
                 [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
                 [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 
        'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], 
                     [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], 
                     [0, 0, 0, 0, 0, 1]], 
        'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
                  [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
                  [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
                  [100, 150, 100, 100, 0, 60]], 
        'store_price': 0.5, 
        'keep_quantity': 100, 
        'n_workhours': 8.0}

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

M = len(num_machines)  # Number of machines
K = len(profit)  # Number of products
I = len(maintain)  # Number of months

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
profit_term = pulp.lpSum(profit[k] * sell[(k, i)] for k in range(K) for i in range(I))
storage_cost_term = pulp.lpSum(store_price * storage[(k, i)] for k in range(K) for i in range(I))
problem += profit_term - storage_cost_term

# Constraints

# Initial storage
for k in range(K):
    problem += storage[(k, 0)] == manufacture[(k, 0)] - sell[(k, 0)]

# Storage balance
for k in range(K):
    for i in range(1, I):
        problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)]

# Storage limitation at end of months
for k in range(K):
    problem += storage[(k, I-1)] == keep_quantity

# Machine time constraints
for i in range(I):
    for m in range(M):
        problem += pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(K)) <= \
                   (num_machines[m] - maintain[i][m]) * n_workhours * 24

# Selling limits
for k in range(K):
    for i in range(I):
        problem += sell[(k, i)] <= limit[k][i]

# Solve
problem.solve()

# Format output
solution = {
    "sell": [[pulp.value(sell[(k, i)]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[(k, i)]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[(k, i)]) for k in range(K)] for i in range(I)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')