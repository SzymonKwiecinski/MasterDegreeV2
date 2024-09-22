import pulp
import json

# Input Data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'down': [1, 1, 1, 1, 1],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

num_m = len(data['num_machines'])
num_p = len(data['profit'])
num_months = len(data['limit'][0])

# Initialize the Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", (range(num_p), range(num_months)), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (range(num_p), range(num_months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(num_p), range(num_months)), lowBound=0, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (range(num_m), range(num_months)), lowBound=0, upBound=1, cat='Binary')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k][i] for k in range(num_p) for i in range(num_months)) - \
            pulp.lpSum(data['store_price'] * storage[k][i] for k in range(num_p) for i in range(num_months))

# Constraints
for k in range(num_p):
    for i in range(num_months):
        problem += sell[k][i] <= data['limit'][k][i]
        
for i in range(num_months):
    available_time = data['n_workhours'] * (24 * 6) * (num_m - sum(data['down']))  # Adjusted for machine down time
    problem += pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(num_p) for m in range(num_m) if data['time'][k][m] > 0) <= available_time

for k in range(num_p):
    for i in range(num_months - 1):
        problem += storage[k][i] + manufacture[k][i] - sell[k][i] == storage[k][i + 1]

for k in range(num_p):
    problem += storage[k][num_months - 1] == data['keep_quantity']
        
# Solve the Problem
problem.solve()

# Print Results
results = {
    "sell": [[pulp.value(sell[k][i]) for k in range(num_p)] for i in range(num_months)],
    "manufacture": [[pulp.value(manufacture[k][i]) for k in range(num_p)] for i in range(num_months)],
    "storage": [[pulp.value(storage[k][i]) for k in range(num_p)] for i in range(num_months)],
    "maintain": [[pulp.value(maintain[m][i]) for m in range(num_m)] for i in range(num_p)]
}

print(json.dumps(results))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')