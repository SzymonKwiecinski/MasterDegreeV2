import pulp
import json

# Define the data from the DATA section
input_data = '''{
"num_machines": [4, 2, 3, 1, 1],
"profit": [10, 6, 8, 4, 11, 9, 3],
"time": [
    [0.5, 0.1, 0.2, 0.05, 0.0],
    [0.7, 0.2, 0.0, 0.03, 0.0],
    [0.0, 0.0, 0.8, 0.0, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.0],
    [0.3, 0.0, 0.0, 0.1, 0.05],
    [0.5, 0.0, 0.6, 0.08, 0.05]
],
"down": [[0, 1, 1, 1, 1]],
"limit": [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
],
"store_price": 0.5,
"keep_quantity": 100,
"n_workhours": 8.0
}'''

data = json.loads(input_data)

# Define sets and indices
M = range(len(data['num_machines']))
K = range(len(data['profit']))
I = range(len(data['limit'][0]))

# Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("Sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("Manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (K, I), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("Maintain", (M, I), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i] for k in K for i in I)

# Constraints
# Selling limits
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i]

# Balance constraints
for k in K:
    for i in I:
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i]
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

# Initial storage
for k in K:
    problem += storage[k][0] == 0

# End storage requirement
for k in K:
    problem += storage[k][len(I) - 1] >= data['keep_quantity']

# Production capacity
for m in M:
    for i in I:
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in K) <= (data['num_machines'][m] - maintain[m][i]) * 24 * 2 * data['n_workhours']

# Maintenance schedule
for m in M:
    problem += pulp.lpSum(maintain[m][i] for i in I) == data['down'][0][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')