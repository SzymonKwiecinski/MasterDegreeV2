import pulp
import json

# Input data in json format
data = {
    'num_machines': [4, 2, 3, 1, 1],
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
    'n_workhours': 8.0
}

# Extracting data
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(num_products) for i in range(num_months)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k, i] for k in range(num_products) for i in range(num_months)) - \
            pulp.lpSum(store_price * storage[k, i] for k in range(num_products) for i in range(num_months))

# Constraints
for i in range(num_months):
    for k in range(num_products):
        # Inventory balance
        if i == 0:
            problem += sell[k, i] - storage[k, i] == manufacture[k, i] - keep_quantity
        else:
            problem += sell[k, i] + storage[k, i - 1] - storage[k, i] == manufacture[k, i] - keep_quantity

        # Marketing limits
        problem += sell[k, i] <= limit[k][i]

    # Time constraints for machines
    total_work_time = pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(num_products) for m in range(len(time[k])))
    available_machines = num_machines - sum(maintain[i][m] for m in range(num_machines))
    problem += total_work_time <= n_workhours * available_machines

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[pulp.value(sell[k, i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k, i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k, i]) for k in range(num_products)] for i in range(num_months)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')