import pulp
import json

# Input data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], [0.0, 0.0, 0.8, 0.0, 0.01], 
             [0.0, 0.3, 0.0, 0.07, 0.0], [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05]],
    'maintain': [[1, 0, 0, 0, 1, 0], [0, 0, 0, 1, 1, 0], [0, 2, 0, 0, 0, 1], 
                 [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]],
    'limit': [[500, 600, 300, 200, 0, 500], [1000, 500, 600, 300, 100, 500], 
              [300, 200, 0, 400, 500, 100], [300, 0, 0, 500, 100, 300], 
              [800, 400, 500, 200, 1000, 1100], [200, 300, 400, 0, 300, 500], 
              [100, 150, 100, 100, 0, 60]],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Parameters
num_m = len(data['num_machines'])
num_k = len(data['profit'])
num_i = len(data['limit'][0])
num_machines_available = [data['num_machines'][m] - sum(data['maintain'][i][m] for i in range(num_i)) for m in range(num_m)]

# Initialize the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_k) for i in range(num_i)), lowBound=0)
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_k) for i in range(num_i)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_k) for i in range(num_i)), lowBound=0)

# Objective function
profit_expr = pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_k) for i in range(num_i)) - \
               pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_k) for i in range(num_i))

problem += profit_expr, "Total Profit"

# Constraints
for i in range(num_i):
    for k in range(num_k):
        problem += sell[k, i] <= data['limit'][k][i], f"Limit_{k}_{i}"
    
    for m in range(num_m):
        problem += pulp.lpSum(data['time[k][m]'] * manufacture[k, i] for k in range(num_k)) <= \
                   num_machines_available[m] * data['n_workhours'] * 24, f"MachineTime_{m}_{i}"

# Inventory flow constraints
for k in range(num_k):
    for i in range(num_i):
        if i == 0:
            problem += storage[k, i] + manufacture[k, i] - sell[k, i] == data['keep_quantity'], f"InventoryFlow_{k}_{i}"
        else:
            problem += storage[k, i-1] + manufacture[k, i] - sell[k, i] == storage[k, i], f"InventoryFlow_{k}_{i}"

# Solve the problem
problem.solve()

# Output results
sell_results = [[pulp.value(sell[k, i]) for k in range(num_k)] for i in range(num_i)]
manufacture_results = [[pulp.value(manufacture[k, i]) for k in range(num_k)] for i in range(num_i)]
storage_results = [[pulp.value(storage[k, i]) for k in range(num_k)] for i in range(num_i)]

output = {
    "sell": sell_results,
    "manufacture": manufacture_results,
    "storage": storage_results
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')