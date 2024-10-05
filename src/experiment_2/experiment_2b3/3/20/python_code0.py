import pulp

# Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1],
        [0, 2, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Constants
K = len(data['profit'])  # Number of products
M = len(data['num_machines'])  # Number of machine types
I = len(data['maintain'])  # Number of months
days_in_month = 24
total_work_hours = data['n_workhours'] * days_in_month

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Continuous')

# Objective Function
profit_expr = pulp.lpSum(
    data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i] for k in range(K) for i in range(I)
)
problem += profit_expr

# Constraints
# Initial storage
for k in range(K):
    problem += storage[k, 0] == manufacture[k, 0] - sell[k, 0]

# Production and storage continuity
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]

# End stock constraint
for k in range(K):
    problem += storage[k, I-1] == data['keep_quantity']

# Machine time constraints
for i in range(I):
    for m in range(M):
        total_available_machine_hours = (data['num_machines'][m] - data['maintain'][i][m]) * total_work_hours
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K)) <= total_available_machine_hours

# Marketing constraints
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]

# Solve problem
problem.solve()

# Output the solution
output = {
    "sell": [[sell[k, i].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[k, i].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[k, i].varValue for k in range(K)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')