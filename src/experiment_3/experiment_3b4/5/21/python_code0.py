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
    'down': [1, 1, 1, 1, 1],
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

num_machines = data['num_machines']
profits = data['profit']
times = data['time']
down = data['down']
limits = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
workhours_available = data['n_workhours']

K = len(profits)  # Number of products
M = len(num_machines)  # Number of machine types
I = len(limits[0])  # Number of months

# Create a problem instance
problem = pulp.LpProblem("Manufacturing_Problem", pulp.LpMaximize)

# Decision Variables
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), 0)
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), 0)
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I+1)), 0)
maintain = pulp.LpVariable.dicts("Maintain", ((m, i) for m in range(M) for i in range(I)), 0, 1, pulp.LpInteger)

# Objective Function
problem += pulp.lpSum(profits[k] * sell[k, i] - store_price * storage[k, i] for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for m in range(M):
        problem += pulp.lpSum(manufacture[k, i] * times[k][m] for k in range(K)) <= (num_machines[m] - maintain[m, i]) * workhours_available

for m in range(M):
    problem += pulp.lpSum(maintain[m, i] for i in range(I)) == down[m]

for k in range(K):
    for i in range(I):
        if i == 0:
            problem += storage[k, i] == manufacture[k, i] - sell[k, i]
        else:
            problem += storage[k, i] == storage[k, i-1] + manufacture[k, i] - sell[k, i]
    problem += storage[k, 0] == 0
    problem += storage[k, I] == keep_quantity
    for i in range(I):
        problem += sell[k, i] <= limits[k][i]
        problem += storage[k, i] <= 100

# Solve the problem
problem.solve()

# Print the objective
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')