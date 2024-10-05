import pulp

# Extract data from JSON
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
    'n_workhours': 8.0,
}

# Indices
products = range(len(data['profit']))
machines = range(len(data['num_machines']))
months = range(len(data['limit'][0]))

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in products for i in months), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in products for i in months), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in products for i in months), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in products for i in months)

# Constraints

# Manufacturing Constraints
for i in months:
    for m in machines:
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in products) <= \
                   (data['num_machines'][m] - data['maintain'][m][i]) * 24 * data['n_workhours'], f"Manufacturing_Constraint_m{m}_i{i}"

# Sales and Stock Constraints
for k in products:
    for i in months:
        problem += sell[k, i] <= data['limit'][k][i], f"Sales_Stock_Constraint_k{k}_i{i}"

# Inventory Balance Constraints
for k in products:
    for i in months:
        if i == 0:
            previous_storage = 0
        else:
            previous_storage = storage[k, i - 1]
        problem += storage[k, i] == previous_storage + manufacture[k, i] - sell[k, i], f"Inventory_Balance_k{k}_i{i}"

# Storage Constraints
for k in products:
    for i in months:
        problem += storage[k, i] <= 100, f"Storage_Constraint_k{k}_i{i}"

# End-of-Period Stock Requirement
for k in products:
    problem += storage[k, months[-1]] == data['keep_quantity'], f"End_Period_Stock_k{k}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')