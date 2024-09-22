import pulp
import json

# Data in JSON format
data_json = '''{'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], 'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], 'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}'''
data = json.loads(data_json)

# Extracting parameters from the data
num_m = sum(data['num_machines'])  # Total number of machines
K = len(data['profit'])  # Number of products
I = len(data['limit'])  # Number of months
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
total_workhours = n_workhours * 6 * 24  # Total available work hours in a month

# Creating the problem variable
problem = pulp.LpProblem("Manufacturing_Profit_Optimization", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for m in range(num_m):
        problem += (pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) 
                     <= total_workhours - sum(maintain[i][m] for m in range(num_m)), f"Machine_Hours_Constraint_{i}_{m}")

for k in range(K):
    for i in range(I):
        problem += (sell[k][i] <= limit[i][k], f"Limit_Constraint_{k}_{i}")
        problem += (storage[k][i] <= 100, f"Storage_Limit_{k}_{i}")

for k in range(K):
    for i in range(1, I):
        problem += (storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Equation_{k}_{i}")

for k in range(K):
    problem += (storage[k][0] == 0, f"Initial_Storage_{k}")

for k in range(K):
    problem += (storage[k][I-1] >= keep_quantity, f"Keep_Quantity_Constraint_{k}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')