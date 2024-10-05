import pulp

# Load the data
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
        [500, 600, 300, 200, 0],
        [1000, 500, 600, 300, 100],
        [300, 200, 0, 400, 500],
        [300, 0, 0, 500, 100],
        [800, 400, 500, 200, 1000],
        [200, 300, 400, 0, 300],
        [100, 150, 100, 100, 0]
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I+1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([data['profit'][k] * sell[(k, i)] - data['store_price'] * storage[(k, i)] for k in range(K) for i in range(I)])

# Constraints
for i in range(I):
    for k in range(K):
        # Market limit constraint
        problem += sell[(k, i)] <= data['limit'][k][i]
        # Manufacture and storage balance
        problem += manufacture[(k, i)] + storage[(k, i)] == sell[(k, i)] + storage[(k, i+1)]

for i in range(I):
    for m in range(M):
        # Production time constraint
        problem += pulp.lpSum([data['time'][k][m] * manufacture[(k, i)] for k in range(K)]) <= data['n_workhours'] * 24 * (data['num_machines'][m] - data['maintain'][i][m])

for k in range(K):
    # Initial and final storage
    problem += storage[(k, 0)] == 0
    problem += storage[(k, I)] == data['keep_quantity']

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "sell": [[pulp.value(sell[(k, i)]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[(k, i)]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[(k, i)]) for k in range(K)] for i in range(I+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')