import pulp
import json

data = {'num_machines': [4, 2, 3, 1, 1], 
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
        'n_workhours': 8.0}

num_m = len(data['num_machines'])
num_k = len(data['profit'])
num_i = len(data['maintain'])
n_workhours = data['n_workhours'] * 24 * 6  # Total working hours in January

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
sell = pulp.LpVariable.dicts("sell", ((k, i) for k in range(num_k) for i in range(num_i)), 
                                    lowBound=0, upBound=None, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", ((k, i) for k in range(num_k) for i in range(num_i)), 
                                                    lowBound=0, upBound=None, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((k, i) for k in range(num_k) for i in range(num_i)), 
                                            lowBound=0, upBound=100, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * sell[k, i] for k in range(num_k) for i in range(num_i)) \
           - pulp.lpSum(data['store_price'] * storage[k, i] for k in range(num_k) for i in range(num_i))

# Constraints
for i in range(num_i):
    # Limit for sales
    for k in range(num_k):
        problem += sell[k, i] <= data['limit'][k][i]

    # Production time constraints
    total_time_available = n_workhours - sum(data['maintain'][i][m] for m in range(num_m))
    for k in range(num_k):
        problem += pulp.lpSum(data['time'][k][m] * manufacture[k, i] for m in range(num_m) if m < len(data['time'][k])) <= total_time_available

    # Storage constraints: Beginning of next month should include the production and storage
    for k in range(num_k):
        if i < num_i - 1:  # Ensure not to access out of index for last month
            problem += storage[k, i] + manufacture[k, i] - sell[k, i] == storage[k, i + 1] + data['keep_quantity']

# Solve the problem
problem.solve()

# Output the results
sell_result = [[sell[k, i].value() for k in range(num_k)] for i in range(num_i)]
manufacture_result = [[manufacture[k, i].value() for k in range(num_k)] for i in range(num_i)]
storage_result = [[storage[k, i].value() for k in range(num_k)] for i in range(num_i)]

output = {
    "sell": sell_result,
    "manufacture": manufacture_result,
    "storage": storage_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')