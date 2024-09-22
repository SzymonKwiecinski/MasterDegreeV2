import pulp

# Data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting parameters
N = range(len(data['processing_times']['central']['isolate']))
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Problem
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in N for j in ['isolate', 'scan']), cat='Binary')
y = pulp.LpVariable.dicts("y", N, cat='Binary')

# Objective Function
problem += pulp.lpSum(
    y[i] * (x[i, 'isolate'] * isolate_central[i] + x[i, 'scan'] * scan_central[i]) * central_cost +
    (1 - y[i]) * (x[i, 'isolate'] * isolate_distributed[i] + x[i, 'scan'] * scan_distributed[i]) * distributed_cost
    for i in N
)

# Constraints
# 1. Intervention Type Consistency
for i in N:
    problem += pulp.lpSum(x[i, j] for j in ['isolate', 'scan']) == 1

# 2. Central Processing Time Constraint
problem += pulp.lpSum(
    y[i] * (x[i, 'isolate'] * isolate_central[i] + x[i, 'scan'] * scan_central[i]) for i in N
) <= max_central

# 3. Distributed Processing Time Constraint
problem += pulp.lpSum(
    (1 - y[i]) * (x[i, 'isolate'] * isolate_distributed[i] + x[i, 'scan'] * scan_distributed[i]) for i in N
) <= max_distributed

# Solve
problem.solve()

# Output
print(f'Status: {pulp.LpStatus[problem.status]}')
for i in N:
    intervention_type = 'isolate' if pulp.value(x[i, 'isolate']) == 1 else 'scan'
    processing_method = 'central' if pulp.value(y[i]) == 1 else 'distributed'
    print(f'Cluster {i+1}: {intervention_type} via {processing_method}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')