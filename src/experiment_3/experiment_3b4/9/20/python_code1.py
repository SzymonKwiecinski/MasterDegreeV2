import pulp

# Given data
data = {
    'num_machines': [4, 2, 3, 1, 1],
    'profit': [10, 6, 8, 4, 11, 9, 3],
    'time': [
        [0.5, 0.1, 0.2, 0.05, 0.0],
        [0.7, 0.2, 0.0, 0.03, 0.0],
        [0.0, 0.0, 0.8, 0.0, 0.01],
        [0.0, 0.3, 0.0, 0.07, 0.0],
        [0.3, 0.0, 0.0, 0.1, 0.05],
        [0.5, 0.0, 0.6, 0.08, 0.05]
    ],
    'maintain': [
        [1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 2, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1]
    ],
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
    'n_workhours': 8.0,
    'days_per_month': 24
}

# Sets
K = range(len(data['profit']))  # Products
M = range(len(data['num_machines']))  # Machines
I = range(len(data['maintain'][0]))  # Months

# Problem
problem = pulp.LpProblem('EngineeringFactory', pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts('sell', (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts('manufacture', (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts('storage', (K, I), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([
    data['profit'][k] * sell[k][i] - data['store_price'] * storage[k][i]
    for k in K for i in I
])

# Constraints
# Machine capacity
for i in I:
    for m in M:
        problem += pulp.lpSum([data['time'][k][m] * manufacture[k][i] for k in K if k < len(data['time'])]) <= \
                   (data['num_machines'][m] - data['maintain'][m][i]) * data['n_workhours'] * data['days_per_month']

# Marketing limitations
for k in K:
    for i in I:
        problem += sell[k][i] <= data['limit'][k][i]

# Inventory balance
for k in K:
    for i in I:
        if i == 0:
            problem += storage[k][i] == manufacture[k][i] - sell[k][i]
        else:
            problem += storage[k][i] == storage[k][i - 1] + manufacture[k][i] - sell[k][i]

# End-of-period stock requirement
for k in K:
    problem += storage[k][len(I) - 1] >= data['keep_quantity']

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')