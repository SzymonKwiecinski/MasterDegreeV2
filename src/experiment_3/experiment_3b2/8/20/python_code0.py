import pulp
import json

# Data from the provided JSON format
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
num_months = len(data['limit'][0])
num_products = len(data['profit'])
num_machines = len(data['num_machines'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)

# Objective Function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months))
storage_cost = pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))
problem += profit_expr - storage_cost

# Machine Capacity Constraints
for m in range(num_machines):
    for i in range(num_months):
        problem += (
            pulp.lpSum(data['time[k][m]'] * manufacture[k][i] for k in range(num_products)) 
            <= (data['num_machines'][m] - data['maintain'][m][i]) * data['n_workhours'] * 24
        )

# Market Limit Constraints
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i]

# Manufacturing and Inventory Balance
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Initial storage condition
for k in range(num_products):
    problem += storage[k][0] == 0

# End of Planning Period Stock Requirement
for k in range(num_products):
    problem += storage[k][num_months - 1] == data['keep_quantity']

# Storage Capacity Constraints
for k in range(num_products):
    for i in range(num_months):
        problem += storage[k][i] <= 100

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')