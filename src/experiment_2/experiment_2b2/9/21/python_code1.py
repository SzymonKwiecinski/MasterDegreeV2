import pulp

# Parse the input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
        [0.0, 0.1, 0.3, 0.06, 0.04]
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

num_products = len(data['profit'])
num_machines = len(data['num_machines'])
num_months = len(data['limit'][0])

# Create the problem variable
problem = pulp.LpProblem('Manufacturing_Optimization', pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(num_machines) for i in range(num_months)), lowBound=0, upBound=1, cat='Integer')

# Objective Function
profit_sum = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_products) for i in range(num_months))
storage_cost = pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_products) for i in range(num_months))
problem += profit_sum - storage_cost

# Constraints
for k in range(num_products):
    # Initial stock constraint
    problem += storage[k, 0] == 0
    for i in range(1, num_months):
        # Balance constraint for manufactured, sold, and stored products
        problem += manufacture[k, i] + storage[k, i - 1] - sell[k, i] == storage[k, i]

    # Final stock constraint
    problem += storage[k, num_months - 1] == data['keep_quantity']

    for i in range(num_months):
        # Marketing limitation constraint
        problem += sell[k, i] <= data['limit'][k][i]

for m in range(num_machines):
    # Ensure maintenance is scheduled correctly, spread across the months
    problem += pulp.lpSum(maintain[m, i] for i in range(num_months)) == data['down'][m]
    for i in range(num_months):
        # Ensure the working time constraint given maintenance
        available_machines = data['num_machines'][m] - maintain[m, i]
        problem += pulp.lpSum(manufacture[k, i] * data['time'][k][m] for k in range(num_products)) <= available_machines * data['n_workhours'] * 24

# Solve the problem
problem.solve()

# Output the result
output = {
    'sell': [[sell[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    'manufacture': [[manufacture[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    'storage': [[storage[k, i].varValue for k in range(num_products)] for i in range(num_months)],
    'maintain': [[maintain[m, i].varValue for m in range(num_machines)] for i in range(num_months)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')