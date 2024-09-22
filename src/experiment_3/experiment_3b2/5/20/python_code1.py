import pulp
import json

# Data from the provided JSON format
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
    'n_workhours': 8.0,
    'n_days': 24
}

# Model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Indices
K = len(data['profit'])
M = len(data['num_machines'])
I = len(data['limit'][0])  # assuming all limits have the same number of months

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] 
                      for k in range(K) for i in range(I))

# Constraints
# Manufacturing Capacity Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K)) \
                   <= (data['num_machines'][m] - data['maintain'][m][i]) * data['n_workhours'] * data['n_days']

# Sales and Storage Constraints
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= data['limit'][k][i]
        if i > 0:
            problem += manufacture[k][i] == sell[k][i] + storage[k][i] - storage[k][i-1]
        else:
            problem += manufacture[k][i] == sell[k][i] + storage[k][i]  # initial month

    problem += storage[k][0] == 0  # initial stock is 0
    problem += storage[k][I-1] == data['keep_quantity']  # final stock is the desired quantity

    # Storage limits
    for i in range(I):
        problem += storage[k][i] <= 100

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')