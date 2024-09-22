import pulp

# Data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {
        'central': 150,
        'distributed': 70
    },
    'max_hours': {
        'central_max_hours': 16,
        'distributed_max_hours': 33
    }
}

N = len(data['processing_times']['central']['isolate'])

# Problem
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Variables
x_central_isolate = [pulp.LpVariable(f'x_{i}_central_isolate', cat='Binary') for i in range(N)]
x_central_scan = [pulp.LpVariable(f'x_{i}_central_scan', cat='Binary') for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f'x_{i}_distributed_isolate', cat='Binary') for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f'x_{i}_distributed_scan', cat='Binary') for i in range(N)]

# Objective Function
costs = data['costs']
processing_times = data['processing_times']
problem += pulp.lpSum([
    processing_times['central']['isolate'][i] * costs['central'] * x_central_isolate[i] +
    processing_times['central']['scan'][i] * costs['central'] * x_central_scan[i] +
    processing_times['distributed']['isolate'][i] * costs['distributed'] * x_distributed_isolate[i] +
    processing_times['distributed']['scan'][i] * costs['distributed'] * x_distributed_scan[i]
    for i in range(N)
])

# Constraints
# Each cluster must have exactly one type of intervention
for i in range(N):
    problem += (
        x_central_isolate[i] + x_central_scan[i] +
        x_distributed_isolate[i] + x_distributed_scan[i] == 1
    )

# Central processing time constraint
problem += pulp.lpSum([
    processing_times['central']['isolate'][i] * x_central_isolate[i] +
    processing_times['central']['scan'][i] * x_central_scan[i]
    for i in range(N)
]) <= data['max_hours']['central_max_hours']

# Distributed processing time constraint
problem += pulp.lpSum([
    processing_times['distributed']['isolate'][i] * x_distributed_isolate[i] +
    processing_times['distributed']['scan'][i] * x_distributed_scan[i]
    for i in range(N)
]) <= data['max_hours']['distributed_max_hours']

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')