import pulp

# Extract the data from the JSON format provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Number of parts and machines
P = len(data['prices'])
M = len(data['availability'])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for the number of batches of each part
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

# Decision variables for extra machine hours
e = pulp.LpVariable.dicts("e", range(M), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
machine_cost = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M)])
extra_hours_cost = pulp.lpSum([data['extra_costs'][m] * e[m] for m in range(M)])

problem += revenue - machine_cost - extra_hours_cost

# Demand constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Machine time constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

# Extra time constraints
for m in range(M):
    problem += e[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')