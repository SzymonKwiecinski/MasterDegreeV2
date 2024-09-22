import pulp
import json

# Data from the provided JSON
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0],
             [0.7, 0.2, 0.0, 0.03, 0.0],
             [0.0, 0.0, 0.8, 0.0, 0.01],
             [0.0, 0.3, 0.0, 0.07, 0.0],
             [0.3, 0.0, 0.0, 0.1, 0.05],
             [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0],
                 [0, 0, 0, 1, 1, 0],
                 [0, 2, 0, 0, 0, 1],
                 [0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1]],
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

# Defining problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Parameters
I = 6  # Number of months
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machines

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(1, I + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(1, I + 1))

# Constraints
# Machine Time Constraint
for i in range(1, I + 1):
    problem += pulp.lpSum(data['time[k][m]'] * manufacture[k, i] for k in range(K) for m in range(M)) <= (data['n_workhours'] * 6 * 24) - pulp.lpSum(data['maintain'][m][i - 1] for m in range(M))

# Marketing Limit Constraint
for k in range(K):
    for i in range(1, I + 1):
        problem += sell[k, i] <= data['limit'][k][i - 1]

# Storage Constraints
for k in range(K):
    for i in range(2, I + 1):
        problem += storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i]
    problem += storage[k, 1] == 0

# Stock Requirement Constraint
for k in range(K):
    problem += storage[k, I] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')