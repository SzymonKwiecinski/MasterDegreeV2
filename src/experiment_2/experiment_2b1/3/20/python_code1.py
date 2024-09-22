import json
import pulp

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0],
             [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01],
             [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05],
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 1, 0],
                 [0, 2, 0, 0, 0, 1],
                 [0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500],
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

num_products = len(data['profit'])
num_months = len(data['limit'][0])
num_machines = len(data['num_machines'])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months)) - \
            pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))

# Constraints
for i in range(num_months):
    # Supply limit constraints
    for k in range(num_products):
        problem += sell[k][i] <= data['limit'][k][i], f"Limit_{k}_{i}"

        if i > 0:
            problem += storage[k][i-1] + manufacture[k][i] - sell[k][i] == storage[k][i], f"Storage_{k}_{i}"

    # Machine time availability
    total_time_used = pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_products) for m in range(num_machines) if (data['num_machines'][m] - data['maintain'][i][m] > 0))
    working_time = (data['n_workhours'] * 6) * (24 - sum(data['maintain'][i][m] for m in range(num_machines)))
    problem += total_time_used <= working_time, f"Time_Availability_{i}"

# Ending storage constraints
for k in range(num_products):
    problem += storage[k][num_months-1] >= data['keep_quantity'], f"Keep_Quantity_{k}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')