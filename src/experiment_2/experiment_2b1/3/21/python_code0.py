import pulp
import json

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
    'down': [1], 
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

num_m = len(data['num_machines'])
profit = data['profit']
time = data['time']
down_period = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
num_months = len(limit[0])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
sell = pulp.LpVariable.dicts("sell", (range(len(profit)), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(len(profit)), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(len(profit)), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_m), range(len(profit))), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([profit[k] * sell[k][i] for k in range(len(profit)) for i in range(num_months)]) - \
           pulp.lpSum([store_price * storage[k][i] for k in range(len(profit)) for i in range(num_months)])

# Constraints

# Production time constraint for each month
for i in range(num_months):
    for m in range(num_m):
        if down_period == m:
            continue
        problem += pulp.lpSum([manufacture[k][i] * time[k][m] for k in range(len(profit))]) <= (n_workhours * 24)

# Selling limits for each product in each month
for k in range(len(profit)):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i]

# Storage constraints
for k in range(len(profit)):
    for i in range(num_months):
        problem += storage[k][i] >= keep_quantity
        
# Solve the problem
problem.solve()

# Output the results
sell_results = [[sell[k][i].varValue for k in range(len(profit))] for i in range(num_months)]
manufacture_results = [[manufacture[k][i].varValue for k in range(len(profit))] for i in range(num_months)]
storage_results = [[storage[k][i].varValue for k in range(len(profit))] for i in range(num_months)]
maintain_results = [[maintain[m][k].varValue for m in range(num_m)] for k in range(len(profit))]

output = {
    "sell": sell_results,
    "manufacture": manufacture_results,
    "storage": storage_results,
    "maintain": maintain_results
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')