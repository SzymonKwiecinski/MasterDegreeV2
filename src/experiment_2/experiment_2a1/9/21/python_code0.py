import json
import pulp

data = {'num_machines': [4, 2, 3, 1, 1], 'profit': [10, 6, 8, 4, 11, 9, 3], 
        'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
                 [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
                 [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]], 
        'down': [[0, 1, 1, 1, 1]], 
        'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
                  [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
                  [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
                  [100, 150, 100, 100, 0, 60]], 
        'store_price': 0.5, 'keep_quantity': 100, 'n_workhours': 8.0}

num_machines = data['num_machines']
profit = data['profit']
time = data['time']
down = data['down'][0]
limit = data['limit']
store_price = data['store_price']
keep_quantity = data['keep_quantity']
n_workhours = data['n_workhours']
total_months = len(limit[0])

M = len(num_machines)
K = len(profit)
I = total_months

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("maintain", ((m, k) for m in range(M) for k in range(K)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(profit[k] * sell[(k, i)] for k in range(K) for i in range(I)) \
           - pulp.lpSum(store_price * storage[(k, i)] for k in range(K) for i in range(I))

# Constraints

# Sales limits by month
for k in range(K):
    for i in range(I):
        problem += sell[(k, i)] <= limit[k][i], f"Sales_Limit_{k}_{i}"

# Production limits based on machine availability
for i in range(I):
    available_time = n_workhours * (6 * 4 - sum(1 for m in range(M) if down[m]))
    problem += (pulp.lpSum(manufacture[(k, i)] * time[k][m] for k in range(K) for m in range(M)) <= available_time), f"Available_Time_{i}"

# Storage constraints
for k in range(K):
    for i in range(I):
        problem += storage[(k, i)] >= keep_quantity, f"Keep_Quantity_{k}_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "sell": [[sell[(k, i)].varValue for k in range(K)] for i in range(I)],
    "manufacture": [[manufacture[(k, i)].varValue for k in range(K)] for i in range(I)],
    "storage": [[storage[(k, i)].varValue for k in range(K)] for i in range(I)],
    "maintain": [[maintain[(m, k)].varValue for k in range(K)] for m in range(M)]
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')