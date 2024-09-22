import pulp
import json

# Input data (converted from JSON format)
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

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
maintain = data['maintain']
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

I = len(limit)  # Number of months
K = len(limit[0])  # Number of products
M = len(num_machines)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0)

# Objective function
problem += pulp.lpSum(profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I))

# Constraints
# Machine time constraint
for i in range(I):
    problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K) for m in range(M)) \
               <= (n_workhours * 24) * (num_machines[m] - sum(maintain[i][m] for m in range(M)))

# Sales limitations
for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[i][k]

# Storage balance equation
for k in range(K):
    for i in range(1, I):
        problem += storage[k][i-1] + manufacture[k][i] - sell[k][i] == storage[k][i]

# Initial storage condition
for k in range(K):
    problem += storage[k][0] == 0

# Final storage requirement
for k in range(K):
    problem += storage[k][I-1] >= keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')