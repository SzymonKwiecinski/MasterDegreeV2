import pulp
import json

# Given data in JSON format
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

I = 6  # number of months
K = len(data['profit'])  # number of products
M = len(data['num_machines'])  # number of machines

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(K)), lowBound=0, cat='Binary')

# Objective function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(K) for i in range(I)) \
            - pulp.lpSum(data['store_price'] * storage[k][i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        problem += sell[k][i] <= data['limit'][k][i], f"Limit_Sell_{k}_{i}"
        
        if i > 0:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i], f"Storage_Balance_{k}_{i}"

        if i == I - 1:
            problem += storage[k][i] >= data['keep_quantity'], f"Final_Stock_{k}"

for m in range(M):
    for i in range(I):
        total_time_needed = pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K))
        problem += total_time_needed <= data['n_workhours'] * (24 - data['down'][m]), f"Machine_Time_{m}_{i}"

# Solve the problem
problem.solve()

# Collecting results
result = {
    "sell": [[sell[k][i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k][i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k][i].varValue for k in range(K)] for i in range(I)],
    "maintain": [[maintain[m][k].varValue for m in range(M)] for k in range(K)]
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')