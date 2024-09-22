import pulp

# Data
processing_times = {
    'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
    'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
}

costs = {'central': 150, 'distributed': 70}
max_hours = {'central': 16, 'distributed': 33}
N = len(processing_times['central']['isolate'])  # Number of clusters

# Problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in range(1, 3) for k in range(1, 3)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    costs['central'] * (x[i, 1, 1] * processing_times['central']['isolate'][i] + x[i, 2, 1] * processing_times['central']['scan'][i]) +
    costs['distributed'] * (x[i, 1, 2] * processing_times['distributed']['isolate'][i] + x[i, 2, 2] * processing_times['distributed']['scan'][i])
    for i in range(N)
)

# Constraints

# Each intervention must be consistent for each cluster
for i in range(N):
    problem += pulp.lpSum(x[i, j, k] for j in range(1, 3) for k in range(1, 3)) == 1

# Central processing time constraint
problem += pulp.lpSum(
    processing_times['central']['isolate'][i] * x[i, 1, 1] + processing_times['central']['scan'][i] * x[i, 2, 1] for i in range(N)
) <= max_hours['central']

# Distributed processing time constraint
problem += pulp.lpSum(
    processing_times['distributed']['isolate'][i] * x[i, 1, 2] + processing_times['distributed']['scan'][i] * x[i, 2, 2] for i in range(N)
) <= max_hours['distributed']

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')