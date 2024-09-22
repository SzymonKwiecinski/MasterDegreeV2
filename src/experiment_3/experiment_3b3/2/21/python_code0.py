import pulp

# Data from JSON
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
    'down': [0, 1, 1, 1, 1],
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
M = len(data['num_machines'])  # Number of machines
K = len(data['profit'])        # Number of products
I = len(data['limit'][0])      # Number of months

# Create the problem
problem = pulp.LpProblem('Engineering_Factory_Problem', pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective Function
problem += pulp.lpSum((data['profit'][k] * sell[k, i] - data['store_price'] * storage[k, i])
                      for k in range(K) for i in range(I))

# Constraints
# Production Time Constraint
for m in range(M):
    for i in range(I):
        problem += (pulp.lpSum(data['time'][k][m] * manufacture[k, i] for k in range(K))
                    <= data['n_workhours'] * (1 - data['down'][m]))

# Marketing Limit Constraint
for k in range(K):
    for i in range(I):
        problem += sell[k, i] <= data['limit'][k][i]

# Storage Balance Equation
for k in range(K):
    for i in range(1, I):
        problem += storage[k, i] == storage[k, i - 1] + manufacture[k, i] - sell[k, i]

# Last month storage level constraint
for k in range(K):
    problem += storage[k, I-1] >= data['keep_quantity']

# Maintenance Constraints
for i in range(I):
    for m in range(M):
        problem += maintain[m, i] <= data['down'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')