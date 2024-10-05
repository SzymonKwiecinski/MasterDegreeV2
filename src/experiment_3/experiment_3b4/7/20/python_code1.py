import pulp

# Data
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
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
    ],
    'limit': [
        [500, 600, 300, 200, 0, 500],
        [1000, 500, 600, 300, 100, 500],
        [300, 200, 0, 400, 500, 100],
        [300, 0, 0, 500, 100, 300],
        [800, 400, 500, 200, 1000, 1100],
        [200, 300, 400, 0, 300, 500],
        [100, 150, 100, 100, 0, 60],
    ],
    'store_price': 0.5,
    'keep_quantity': 100,
    'n_workhours': 8.0
}

# Sets
M = range(len(data['num_machines']))  # Machines
K = range(len(data['profit']))       # Products
I = range(len(data['maintain'][0]))  # Months

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, i) for k in K for i in I), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, i) for k in K for i in I), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("s", ((k, i) for k in K for i in I), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['profit'][k] * y[k, i] - data['store_price'] * s[k, i] for k in K for i in I)

# Constraints

# Manufacturing Constraints
for i in I:
    for m in M:
        problem += pulp.lpSum(data['time'][k][m] * x[k, i] for k in K if k < len(data['time'])) <=\
                   24 * data['n_workhours'] * (data['num_machines'][m] - data['maintain'][i][m])

# Sales Constraints
for k in K:
    for i in I:
        problem += y[k, i] <= data['limit'][k][i]

# Inventory Balance
for k in K:
    for i in I:
        if i > 0:
            problem += s[k, i-1] + x[k, i] == y[k, i] + s[k, i]
        else:
            problem += x[k, i] == y[k, i] + s[k, i]

# Storage Limitation
for k in K:
    for i in I:
        problem += s[k, i] <= 100

# End of Month Stock Requirement
for k in K:
    problem += s[k, I[-1]] == data['keep_quantity']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')