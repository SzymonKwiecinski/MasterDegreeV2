import pulp
import json

# Load the data from JSON format
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Define problem
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines
I = len(data['limit'][0])  # Number of months

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I))

# Constraints
for m in range(M):
    for i in range(I):
        problem += maintain[m, i] <= data['down'][0][m]  # Maintenance constraints
        
        problem += pulp.lpSum(manufacture[k, i] * data['time'][k][m] for k in range(K)) <= (data['num_machines'][m] - maintain[m, i]) * 24 * 2 * data['n_workhours']  # Production capacity constraints
        
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]  # Selling limits
        problem += storage[k, i] <= 100  # Storage limit
        
        if i > 0:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]  # Storage balance
        else:
            problem += storage[k, i] == 0  # Initial storage condition
            
    problem += storage[k, I-1] == data['keep_quantity']  # End-of-month storage condition

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')