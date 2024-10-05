import pulp

# Data
data = {
    'processing_times': {
        'central': {
            'isolate': [10, 6, 8],
            'scan': [6, 4, 6]
        },
        'distributed': {
            'isolate': [12, 9, 12],
            'scan': [18, 10, 15]
        }
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

# Parameters
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']
N = len(data['processing_times']['central']['isolate'])

# Problem setup
problem = pulp.LpProblem("NetworkIntervention", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']], cat='Binary')

# Objective function
problem += pulp.lpSum([
    x[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] * central_cost +
    x[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i] * central_cost +
    x[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] * distributed_cost +
    x[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i] * distributed_cost
    for i in range(N)
])

# Constraints
for i in range(N):
    # Each cluster must have exactly one intervention
    problem += pulp.lpSum([x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']]) == 1

# Maximum hours for central processing
problem += pulp.lpSum([
    x[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] +
    x[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i]
    for i in range(N)
]) <= max_central

# Maximum hours for distributed processing
problem += pulp.lpSum([
    x[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] +
    x[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
]) <= max_distributed

# Solve the problem
problem.solve()

# Output
interventions = []
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(x[i, j, k]) == 1:
                interventions.append({
                    "cluster_id": i + 1,
                    "type": j,
                    "method": k,
                    "amount": 1
                })

total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')