import pulp

# Extracting data from JSON
data = {
    'num_machines': [4, 2, 3, 1, 1], 
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

num_months = 6
num_products = len(data['profit'])
num_machines = len(data['num_machines'])

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months + 1)), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[(k, i)] for k in range(num_products) for i in range(num_months)) - \
           pulp.lpSum(data['store_price'] * storage[(k, i)] for k in range(num_products) for i in range(num_months)), "Total Profit"

# Constraints
for i in range(num_months):
    # Machine Time Constraint
    problem += pulp.lpSum(data['time'][m][k] * manufacture[(k, i)] for k in range(num_products) for m in range(num_machines)) <= \
               data['n_workhours'] * 6 * (24 - sum(data['maintain'][m][i] for m in range(num_machines))), f"Machine_Time_{i}"

    for k in range(num_products):
        # Selling Limits
        problem += sell[(k, i)] <= data['limit'][k][i], f"Selling_Limit_{k}_{i}"

        # Storage Constraints
        if i == 0:
            problem += storage[(k, i)] == manufacture[(k, i)] - sell[(k, i)], f"Storage_Constraint_Init_{k}_{i}"
        else:
            problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)], f"Storage_Constraint_{k}_{i}"

        # Storage upper limit
        problem += storage[(k, i)] <= 100, f"Storage_Upper_{k}_{i}"

# End-of-Month Stock Requirements
for k in range(num_products):
    problem += storage[(k, num_months-1)] >= data['keep_quantity'], f"End_Month_Stock_{k}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')