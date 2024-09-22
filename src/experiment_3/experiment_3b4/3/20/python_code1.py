import pulp

# Problem data
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
days_per_month = 24
num_products = len(data['profit'])
num_machines = len(data['num_machines'])
num_months = len(data['limit'][0])

# Create a linear programming problem
problem = pulp.LpProblem("Production_And_Storage_Optimization", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, upBound=100, cat='Continuous')

# Objective function
profit_terms = [
    data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i]
    for k in range(num_products) for i in range(num_months)
]
problem += pulp.lpSum(profit_terms)

# Constraints

# Machine time constraints
for i in range(num_months):
    for m in range(num_machines):
        problem += pulp.lpSum(data['time'][m][k] * manufacture[k, i] for k in range(num_products)) <= \
                   (data['num_machines'][m] - data['maintain'][m][i]) * data['n_workhours'] * days_per_month

# Product balance constraints
for k in range(num_products):
    for i in range(num_months):
        if i == 0:
            problem += manufacture[k, i] == sell[k, i] + storage[k, i]
        else:
            problem += storage[k, i-1] + manufacture[k, i] == sell[k, i] + storage[k, i]

# Marketing limitations
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k, i] <= data['limit'][k][i]

# Final storage requirement
for k in range(num_products):
    problem += storage[k, num_months - 1] == data['keep_quantity']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')