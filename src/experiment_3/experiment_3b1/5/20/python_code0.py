import pulp
import json

# Data provided in JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "maintain": [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Extract parameters from data
M = len(data['num_machines'])        # Number of machines
K = len(data['profit'])               # Number of products
I = len(data['limit'])                # Number of months

profit = data['profit']               # Profit from products
time = data['time']                   # Production time for products on machines
maintain = data['maintain']           # Maintenance data
limit = data['limit']                 # Marketing limitations
store_price = data['store_price']     # Storage cost
keep_quantity = data['keep_quantity'] # Desired stock
n_workhours = data['n_workhours']     # Hours of work per day
N = 24                                 # Days in a month

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum((profit[k] * sell[k, i] - store_price * storage[k, i]) for k in range(K) for i in range(I))

# Constraints
# 1. Production time constraint
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k, i] for k in range(K)) <= (n_workhours * 6 * (24 - maintain[i][m]))

# 2. Marketing limitation
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= limit[i][k]

# 3. Relation between sell, manufacture and storage
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i - 1] + manufacture[k, i] - sell[k, i] == storage[k, i]

# 4. End of month storage requirement
for k in range(K):
    problem += storage[k, I - 1] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')