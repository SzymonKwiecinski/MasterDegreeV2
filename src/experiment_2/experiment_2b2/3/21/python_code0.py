import pulp

# Problem data
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
        [0.6, 0.0, 0.0, 0.1, 0.0]
    ],
    'down': [0, 1, 1, 1, 1],
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

# Derive constants from data
M = len(data['num_machines'])  # Number of machine types
K = len(data['profit'])        # Number of product types
I = len(data['limit'][0])      # Number of months

# Initialize a MILP problem
problem = pulp.LpProblem("Factory_Optimization", pulp.LpMaximize)

# Decision variables
manufacture = pulp.LpVariable.dicts("Manufacture", (range(K), range(I)), lowBound=0, cat='Integer')
sell = pulp.LpVariable.dicts("Sell", (range(K), range(I)), lowBound=0, cat='Integer')
storage = pulp.LpVariable.dicts("Storage", (range(K), range(I)), lowBound=0, cat='Integer')
maintain = pulp.LpVariable.dicts("Maintain", (range(M), range(I)), lowBound=0, cat='Integer')

# Objective function
profit_terms = []
store_cost_terms = []
for i in range(I):
    profit_terms += [data['profit'][k] * sell[k][i] for k in range(K)]
    store_cost_terms += [data['store_price'] * storage[k][i] for k in range(K)]

problem += pulp.lpSum(profit_terms) - pulp.lpSum(store_cost_terms)

# Constraints
for i in range(I):
    for m in range(M):
        available_machine_hours = data['num_machines'][m] * data['n_workhours'] * 24
        unavailable_hours_due_to_maintenance = maintain[m][i] * data['n_workhours'] * 24
        
        machine_time_used = pulp.lpSum(data['time'][k][m] * manufacture[k][i] for k in range(K))
        problem += machine_time_used <= (available_machine_hours - unavailable_hours_due_to_maintenance)
        
        # Maintenance constraints
        if i + data["down"][m] < I:
            problem += pulp.lpSum(maintain[m][j] for j in range(i, i + data["down"][m])) == maintain[m][i + data["down"][m]]

    for k in range(K):
        # Manufacturing less than or equal to marketing limit
        problem += manufacture[k][i] <= data['limit'][k][i]
        
        # Inventory flow constraints
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i]
        else:
            problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]

        # Storage capacity constraint
        problem += storage[k][i] <= 100

# End of period stock requirement
for k in range(K):
    problem += storage[k][I - 1] >= data['keep_quantity']

# Solve the problem
problem.solve()

# Output the results
result = {
    "sell": [[sell[k][i].varValue for i in range(I)] for k in range(K)],
    "manufacture": [[manufacture[k][i].varValue for i in range(I)] for k in range(K)],
    "storage": [[storage[k][i].varValue for i in range(I)] for k in range(K)],
    "maintain": [[maintain[m][i].varValue for i in range(I)] for m in range(M)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')