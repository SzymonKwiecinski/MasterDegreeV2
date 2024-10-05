import pulp

# Data from JSON
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
    'down': [[0, 1, 1, 1, 1]],
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

# Constants
K = len(data['profit'])  # Number of products
M = len(data['time'][0])  # Number of machines
I = len(data['limit'][0])  # Number of months

# Indices
products = range(K)
machines = range(M)
months = range(I)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in products for i in months), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in products for i in months), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in products for i in months), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", ((m, k, i) for m in machines for k in products for i in months), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in products for i in months)

# Constraints

# Production Capacity Constraint
for m in machines:
    for i in months:
        problem += (
            pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in products) <= 
            data['n_workhours'] * (6 * 2 - sum(data['down'][0][:i+1])),
            f"ProductionCapacity_Machine_{m}_Month_{i}"
        )

# Sales Limitation Constraint
for k in products:
    for i in months:
        problem += (
            sell[k, i] <= data['limit'][k][i],
            f"SalesLimit_Product_{k}_Month_{i}"
        )

# Storage Balance Constraint
for k in products:
    for i in months:
        if i == 0:
            problem += (
                storage[k, i] == manufacture[k, i] - sell[k, i],
                f"StorageBalance_Product_{k}_Month_{i}"
            )
        else:
            problem += (
                storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i],
                f"StorageBalance_Product_{k}_Month_{i}"
            )

# Ending Inventory Constraint
for k in products:
    problem += (
        storage[k, I - 1] >= data['keep_quantity'],
        f"EndingInventory_Product_{k}"
    )

# Maintenance Scheduling Constraint
for m in machines:
    available_machines = data['num_machines'][m] - sum(data['down'][0][:I])
    for k in products:
        for i in months:
            problem += (
                maintain[m, k, i] <= available_machines,
                f"MaintenanceScheduling_Machine_{m}_Product_{k}_Month_{i}"
            )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')