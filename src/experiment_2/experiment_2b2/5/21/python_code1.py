import pulp

# Data from JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
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
        [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Problem parameters
M = len(data['num_machines'])  # Number of machine types
K = len(data['profit'])        # Number of products
I = len(data['limit'][0])      # Number of months
DAYS_IN_MONTH = 24             # Number of working days in a month
SHIFT_PER_DAY = 2              # Two shifts per day

# Total working hours in a month
total_workhours_month = DAYS_IN_MONTH * SHIFT_PER_DAY * data['n_workhours']

# Create the linear problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat=pulp.LpInteger)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat=pulp.LpInteger)
maintain = pulp.LpVariable.dicts("maintain", ((m, k) for m in range(M) for k in range(K)), lowBound=0, cat=pulp.LpInteger)

# Objective function: Maximize profit
profit_terms = [data['profit'][k] * sell[(k, i)] for k in range(K) for i in range(I)]
storage_costs = [data['store_price'] * storage[(k, i)] for k in range(K) for i in range(I)]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(storage_costs), "Total_Profit"

# Constraints

# Production and maintenance constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[(k, i)] for k in range(K) if m < len(data['time'][k])) <= \
                   (data['num_machines'][m] - data['down'][m]) * total_workhours_month

# Market limits
for k in range(K):
    for i in range(I):
        problem += sell[(k, i)] <= data['limit'][k][i]

# Balance constraints between manufactured, sold, and stored goods
for k in range(K):
    for i in range(I):
        if i == 0:  # No inventory at the start
            problem += manufacture[(k, i)] == sell[(k, i)] + storage[(k, i)]
        else:
            problem += manufacture[(k, i)] + storage[(k, i-1)] == sell[(k, i)] + storage[(k, i)]

# Ending stock requirement
for k in range(K):
    problem += storage[(k, I-1)] >= data['keep_quantity']

# Length of Maintenance for Machines
for m in range(M):
    problem += pulp.lpSum(maintain[(m, k)] for k in range(K)) <= data['down'][m]

# Solve the problem
problem.solve()

# Output results
output = {
    "sell": [[pulp.value(sell[(k, i)]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[(k, i)]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[(k, i)]) for k in range(K)] for i in range(I)],
    "maintain": [[pulp.value(maintain[(m, k)]) for m in range(M)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')