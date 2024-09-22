import pulp

# Data extraction
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

N = len(data['processing_times']['central']['isolate'])

# Variables
central_isolate_times = data['processing_times']['central']['isolate']
central_scan_times = data['processing_times']['central']['scan']
distributed_isolate_times = data['processing_times']['distributed']['isolate']
distributed_scan_times = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Problem
problem = pulp.LpProblem("NetworkIntrusionIntervention", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", 
    ((i, j, k) for i in range(N) 
               for j in ['isolate', 'scan'] 
               for k in ['central', 'distributed']), 
    cat='Binary')

# Objective Function
problem += pulp.lpSum([
    central_cost * (central_isolate_times[i] * x[i, 'isolate', 'central'] + 
                    central_scan_times[i] * x[i, 'scan', 'central']) +
    distributed_cost * (distributed_isolate_times[i] * x[i, 'isolate', 'distributed'] + 
                        distributed_scan_times[i] * x[i, 'scan', 'distributed'])
    for i in range(N)
])

# Constraints
# Each cluster must have exactly one intervention method
for i in range(N):
    problem += pulp.lpSum([
        x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']
    ]) == 1

# Central processing time constraint
problem += pulp.lpSum([
    central_isolate_times[i] * x[i, 'isolate', 'central'] + 
    central_scan_times[i] * x[i, 'scan', 'central']
    for i in range(N)
]) <= max_central

# Distributed processing time constraint
problem += pulp.lpSum([
    distributed_isolate_times[i] * x[i, 'isolate', 'distributed'] + 
    distributed_scan_times[i] * x[i, 'scan', 'distributed']
    for i in range(N)
]) <= max_distributed

# Solve
problem.solve()

# Objective value output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')