import pulp
import json

# Load the data
data = json.loads('{"num_machines": [4, 2, 3, 1, 1], "profit": [10, 6, 8, 4, 11, 9, 3], "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], "down": [[0, 1, 1, 1, 1]], "limit": [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], [100, 150, 100, 100, 0, 60]], "store_price": 0.5, "keep_quantity": 100, "n_workhours": 8.0}')

# Parameters
num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']

I = len(limit[0])
K = len(profit)
M = len(num_machines)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
manufacture = pulp.LpVariable.dicts("manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("sell", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", (range(K), range(I)), lowBound=0, upBound=100, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum((profit[k] * sell[k][i] - store_price * storage[k][i] for k in range(K) for i in range(I)))

# Constraints
for m in range(M):
    for i in range(I):
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in range(K)) <= (num_machines[m] - maintain[m][i]) * n_workhours * 24
        
for m in range(M):
    problem += pulp.lpSum(maintain[m][i] for i in range(I)) == down[m]

for k in range(K):
    for i in range(I):
        problem += sell[k][i] <= limit[k][i]
        if i > 0:
            problem += manufacture[k][i] + storage[k][i - 1] == sell[k][i] + storage[k][i]

for k in range(K):
    problem += storage[k][0] == 0
    problem += storage[k][I - 1] == keep_quantity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')