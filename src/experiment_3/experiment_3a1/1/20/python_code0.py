import pulp
import json

# Load the data from JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Extract data
num_m = len(data['num_machines'])
num_k = len(data['profit'])
num_i = len(data['limit'][0])  # Assuming each limit has the same length
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

# Initialize the problem
problem = pulp.LpProblem("Factory_Problem", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_k), range(num_i)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_k), range(num_i)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_k), range(num_i)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] - store_price * storage[k][i] for k in range(num_k) for i in range(num_i))

# Constraints
# Production Time Constraint
for i in range(num_i):
    problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_k) for m in range(num_m)) <= (n_workhours * 6 * 24) - pulp.lpSum(data['maintain'][i][m] for m in range(num_m))

# Marketing Limitation
for k in range(num_k):
    for i in range(num_i):
        problem += sell[k][i] <= data['limit'][k][i]

# Inventory Balance
for k in range(num_k):
    for i in range(1, num_i):
        problem += storage[k][i-1] + manufacture[k][i] - sell[k][i] == storage[k][i]

# Ending Inventory Requirement
for k in range(num_k):
    problem += storage[k][num_i - 1] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')