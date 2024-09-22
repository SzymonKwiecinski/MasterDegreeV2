import pulp

# Load the data from the JSON format provided
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05],
        [0.2, 0.1, 0.0, 0.0, 0.05]
    ],
    'down': [[0, 1, 1, 1, 1]],
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

# Extracting data
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

M = len(num_machines)  # Number of machine types
K = len(profit)        # Number of products
I = len(limit[0])      # Number of months

# Total work hours in a month
total_workhours = 2 * 6 * n_workhours * 24

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintenance", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(profit[k] * sell[(k, i)] - store_price * storage[(k, i)] for k in range(K) for i in range(I))

# Constraints
# Inventory constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += storage[(k, i)] == manufacture[(k, i)] - sell[(k, i)]
        else:
            problem += storage[(k, i)] == storage[(k, i-1)] + manufacture[(k, i)] - sell[(k, i)]
        problem += sell[(k, i)] <= limit[k][i]

# Machine constraints
for m in range(M):
    for i in range(I):
        problem += (
            pulp.lpSum(time[k][m] * manufacture[(k, i)] for k in range(K))
            <= total_workhours * (num_machines[m] - maintain[(m, i)])
        )

# Maintenance constraints
for m in range(M):
    problem += pulp.lpSum(maintain[(m, i)] for i in range(I)) == down[m]

# Final stock constraints
for k in range(K):
    problem += storage[(k, I-1)] == keep_quantity

# Solve the problem
problem.solve()

# Collect the results
result = {
    'sell': [[pulp.value(sell[(k, i)]) for k in range(K)] for i in range(I)],
    'manufacture': [[pulp.value(manufacture[(k, i)]) for k in range(K)] for i in range(I)],
    'storage': [[pulp.value(storage[(k, i)]) for k in range(K)] for i in range(I)],
    'maintain': [[pulp.value(maintain[(m, i)]) for m in range(M)] for i in range(I)]
}

print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')