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
    'n_workhours': 8.0
}

# Constants
months = len(data['maintain'])
products = len(data['profit'])
machines = len(data['num_machines'])
days_per_month = 24

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(products) for i in range(months)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(products) for i in range(months)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(products) for i in range(months)), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(
    [data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(products) for i in range(months)]
)
problem += profit

# Constraints
for i in range(months):
    for k in range(products):
        if i == 0:
            problem += manufacture[k, i] == sell[k, i] + storage[k, i]
        else:
            problem += manufacture[k, i] + storage[k, i - 1] == sell[k, i] + storage[k, i]
        problem += sell[k, i] <= data['limit'][k][i]

    for m in range(machines):
        available_hours = (data['num_machines'][m] - data['maintain'][i][m]) * data['n_workhours'] * days_per_month
        problem += pulp.lpSum([data['time'][k][m] * manufacture[k, i] for k in range(products)]) <= available_hours

# Ending stock constraints
for k in range(products):
    problem += storage[k, months - 1] == data['keep_quantity']

# Solve the problem
problem.solve()

# Extract results
result = {
    "sell": [[int(sell[k, i].varValue) for k in range(products)] for i in range(months)],
    "manufacture": [[int(manufacture[k, i].varValue) for k in range(products)] for i in range(months)],
    "storage": [[int(storage[k, i].varValue) for k in range(products)] for i in range(months)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')