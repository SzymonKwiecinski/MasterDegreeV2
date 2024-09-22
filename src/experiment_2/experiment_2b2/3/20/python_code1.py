from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
import json

# Load the JSON data
data_json = '''{
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    "maintain": [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 2, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    "limit": [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}'''

data = json.loads(data_json)

# Extract data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Constants
num_products = len(profit)
num_machines_total = len(num_machines)
num_months = len(maintain)
days_per_month = 24

# Define problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Variables
manufacture = LpVariable.dicts("Manufacture", (range(num_products), range(num_months)), lowBound=0, cat='Integer')
sell = LpVariable.dicts("Sell", (range(num_products), range(num_months)), lowBound=0, cat='Integer')
storage = LpVariable.dicts("Storage", (range(num_products), range(num_months)), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit_terms = []
for k in range(num_products):
    for i in range(num_months):
        sell_profit = profit[k] * sell[k][i]
        storage_cost = store_price * storage[k][i]
        profit_terms.append(sell_profit - storage_cost)

problem += lpSum(profit_terms)

# Constraints
# Initial storage
for k in range(num_products):
    problem += storage[k][0] == manufacture[k][0] - sell[k][0]

# Storage balance
for k in range(num_products):
    for i in range(1, num_months):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Keep a stock of keep_quantity at the end of the last month
for k in range(num_products):
    problem += storage[k][num_months - 1] >= keep_quantity

# Machine availability and production capacity constraints
for i in range(num_months):
    for m in range(num_machines_total):
        available_machines = num_machines[m] - maintain[i][m]
        max_hours = available_machines * n_workhours * days_per_month
        time_consumed = lpSum(time[k][m] * manufacture[k][i] for k in range(num_products))
        problem += time_consumed <= max_hours

# Marketing limits
for k in range(num_products):
    for i in range(num_months):
        problem += sell[k][i] <= limit[k][i]

# Solve the problem
problem.solve()

# Extract results
sell_result = [[int(sell[k][i].varValue) for k in range(num_products)] for i in range(num_months)]
manufacture_result = [[int(manufacture[k][i].varValue) for k in range(num_products)] for i in range(num_months)]
storage_result = [[int(storage[k][i].varValue) for k in range(num_products)] for i in range(num_months)]

result = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

# Print results
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')