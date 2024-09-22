import pulp

# Data as per given format
data = {
    "num_machines": [4, 2, 3, 1, 1],
    "profit": [10, 6, 8, 4, 11, 9, 3],
    "time": [[0.5, 0.1, 0.2, 0.05, 0.0], [0.7, 0.2, 0.0, 0.03, 0.0], 
             [0.0, 0.0, 0.8, 0.0, 0.01], [0.0, 0.3, 0.0, 0.07, 0.0], 
             [0.3, 0.0, 0.0, 0.1, 0.05], [0.5, 0.0, 0.6, 0.08, 0.05], 
             [0.1, 0.0, 0.3, 0.04, 0.02]],  # added consistent time entries
    "maintain": [[1, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 2, 0, 0, 0], 
                 [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],  # corrected missing columns
    "limit": [[500, 600, 300, 200, 0], [1000, 500, 600, 300, 100], 
              [300, 200, 0, 400, 500], [300, 0, 0, 500, 100], 
              [800, 400, 500, 200, 1000], [200, 300, 400, 0, 300], 
              [100, 150, 100, 100, 0]],  # corrected dimensions
    "store_price": 0.5,
    "keep_quantity": 100,
    "n_workhours": 8.0
}

# Constants
M = len(data['num_machines'])
K = len(data['profit'])
I = len(data['limit'][0])
days_in_month = 24

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
manufacture = pulp.LpVariable.dicts("Manufacture", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", ((k, i) for k in range(K) for i in range(I + 1)), lowBound=0, cat='Integer')

# Objective Function
profit_terms = [data['profit'][k] * sell[(k, i)] for k in range(K) for i in range(I)]
storage_costs = [-data['store_price'] * storage[(k, i + 1)] for k in range(K) for i in range(I)]
problem += pulp.lpSum(profit_terms) + pulp.lpSum(storage_costs)

# Constraints
for i in range(I):
    for k in range(K):
        # Selling constraint
        problem += sell[(k, i)] <= data['limit'][k][i]
        
        # Inventory balance constraint
        if i == 0:
            problem += storage[(k, i)] == 0
        else:
            problem += storage[(k, i)] == storage[(k, i - 1)] + manufacture[(k, i)] - sell[(k, i)]
        if i < I - 1:
            problem += storage[(k, i + 1)] == storage[(k, i)] + manufacture[(k, i + 1)] - sell[(k, i + 1)]

# Ending inventory constraint for each month
for k in range(K):
    problem += storage[(k, I)] == data['keep_quantity']

# Machine time constraints
for i in range(I):
    for m in range(M):
        available_hours = (data['num_machines'][m] - data['maintain'][i][m]) * data['n_workhours'] * days_in_month
        problem += pulp.lpSum([data['time'][k][m] * manufacture[(k, i)] for k in range(K)]) <= available_hours

# Solve the problem
problem.solve()

# Collecting results
output = {
    "sell": [[pulp.value(sell[(k, i)]) for k in range(K)] for i in range(I)],
    "manufacture": [[pulp.value(manufacture[(k, i)]) for k in range(K)] for i in range(I)],
    "storage": [[pulp.value(storage[(k, i)]) for k in range(K)] for i in range(I + 1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')