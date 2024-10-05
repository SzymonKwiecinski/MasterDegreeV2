from pulp import LpMaximize, LpProblem, LpVariable, lpSum

# Data input
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
        [0.1, 0.2, 0.0, 0.09, 0.0]
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

# Problem setup
num_months = len(data['limit'][0])
num_products = len(data['profit'])
num_machines = len(data['num_machines'])

# Machine variables
manufacture = LpVariable.dicts("manufacture", (range(num_products), range(num_months)), 0, None)
sell = LpVariable.dicts("sell", (range(num_products), range(num_months)), 0, None)
storage = LpVariable.dicts("storage", (range(num_products), range(num_months)), 0, 100)
maintain = LpVariable.dicts("maintain", (range(num_machines), range(num_months)), 0, None, cat='Integer')

# Initialize the problem
problem = LpProblem("Manufacturing_Profit_Maximization", LpMaximize)

# Objective function
problem += lpSum([data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] 
                  for k in range(num_products) for i in range(num_months)])

# Constraints

# Manufacturing constraints
for i in range(num_months):
    for m in range(num_machines):
        problem += lpSum([data['time'][k][m] * manufacture[k][i] for k in range(num_products)]) <= (
            data['num_machines'][m] - maintain[m][i]) * 24 * data['n_workhours']

# Maintainance constraints
for m in range(num_machines):
    problem += lpSum([maintain[m][i] for i in range(num_months)]) == data['down'][m]

# Storage flow constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i]
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Product limits constraints
for i in range(num_months):
    for k in range(num_products):
        problem += sell[k][i] <= data['limit'][k][i]
    for k in range(num_products):
        problem += store_price[k][i] <= data['store_price']

# End-of-period stock constraints
for k in range(num_products):
    problem += storage[k][num_months - 1] == data['keep_quantity']

# Solve the problem
problem.solve()

# Output the solution
output = {
    "sell": [[sell[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[manufacture[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "storage": [[storage[k][i].varValue for k in range(num_products)] for i in range(num_months)],
    "maintain": [[maintain[m][i].varValue for m in range(num_machines)] for i in range(num_months)]
}

print(f'Output: {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')