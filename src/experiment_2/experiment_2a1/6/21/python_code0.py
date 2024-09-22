import pulp
import json

# Input data
data = {'num_machines': [4, 2, 3, 1, 1], 
        'profit': [10, 6, 8, 4, 11, 9, 3], 
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], 
                 [0.7, 0.2, 0.0, 0.03, 0.0], 
                 [0.0, 0.0, 0.8, 0.0, 0.01], 
                 [0.0, 0.3, 0.0, 0.07, 0.0], 
                 [0.3, 0.0, 0.0, 0.1, 0.05], 
                 [0.5, 0.0, 0.6, 0.08, 0.05]], 
        'down': [[0, 1, 1, 1, 1]], 
        'limit': [[500, 600, 300, 200, 0, 500], 
                  [1000, 500, 600, 300, 100, 500], 
                  [300, 200, 0, 400, 500, 100], 
                  [300, 0, 0, 500, 100, 300], 
                  [800, 400, 500, 200, 1000, 1100], 
                  [200, 300, 400, 0, 300, 500], 
                  [100, 150, 100, 100, 0, 60]], 
        'store_price': 0.5, 
        'keep_quantity': 100, 
        'n_workhours': 8.0}

num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
n_workhours = data['n_workhours']
down_time = data['down'][0]

# Create the LP problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), lowBound=0, upBound=1, cat='Binary')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_products) for i in range(num_months)) - \
            pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_products) for i in range(num_months))

# Constraints
for i in range(num_months):
    for k in range(num_products):
        problem += sell[k][i] <= data['limit'][k][i]  # Market Limit

    for m in range(num_machines):
        if i >= down_time[m]:
            machine_time = pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_products))
            problem += machine_time <= (n_workhours * (24 - down_time[m]) if i == 0 else n_workhours * 24)

for k in range(num_products):
    problem += storage[k][num_months - 1] >= data['keep_quantity']  # Keeping stock at the end of the last month

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_products)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_products)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_products)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(num_machines)] for i in range(num_products)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')