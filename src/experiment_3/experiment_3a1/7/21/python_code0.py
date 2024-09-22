import pulp
import json

# Load data
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Extract data
num_machines = len(data['num_machines'])
num_products = len(data['profit'])
num_months = len(data['limit'][0])
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_products), range(num_months)), lowBound=0)
sell = pulp.LpVariable.dicts("sell", (range(num_products), range(num_months)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(num_products), range(num_months)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", (range(num_machines), range(num_months)), cat='Binary')

# Objective function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(num_products) for i in range(num_months))

# Constraints
for m in range(num_machines):
    for i in range(num_months):
        problem += (pulp.lpSum(manufacture[k][i] * time[k][m] for k in range(num_products)) 
                     <= n_workhours * 12 * (24 - down[m]))

for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i]

for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

for k in range(num_products):
    problem += storage[k][0] == 0

for k in range(num_products):
    problem += storage[k][num_months - 1] >= keep_quantity

for m in range(num_machines):
    problem += pulp.lpSum(maintain[m][i] for i in range(num_months)) <= down[m]

for k in range(num_products):
    for i in range(num_months):
        problem += manufacture[k][i] >= 0
        problem += sell[k][i] >= 0
        problem += storage[k][i] >= 0

for m in range(num_machines):
    for i in range(num_months):
        maintain[m][i].cat = pulp.LpBinary

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')