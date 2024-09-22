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

N = len(data['processing_times']['central']['isolate'])  # Number of clusters

# Create the LP problem
problem = pulp.LpProblem("Minimize_Processing_Cost", pulp.LpMinimize)

# Decision Variables
x_isolate_central = pulp.LpVariable.dicts("x_isolate_central", range(N), cat='Binary')
x_scan_central = pulp.LpVariable.dicts("x_scan_central", range(N), cat='Binary')
x_isolate_distributed = pulp.LpVariable.dicts("x_isolate_distributed", range(N), cat='Binary')
x_scan_distributed = pulp.LpVariable.dicts("x_scan_distributed", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum([
    data['costs']['central'] * (x_isolate_central[i] * data['processing_times']['central']['isolate'][i] +
                                x_scan_central[i] * data['processing_times']['central']['scan'][i]) +
    data['costs']['distributed'] * (x_isolate_distributed[i] * data['processing_times']['distributed']['isolate'][i] +
                                    x_scan_distributed[i] * data['processing_times']['distributed']['scan'][i])
    for i in range(N)
])

# Constraints
for i in range(N):
    problem += (x_isolate_central[i] + x_scan_central[i] +
                x_isolate_distributed[i] + x_scan_distributed[i] == 1)

problem += pulp.lpSum([
    x_isolate_central[i] * data['processing_times']['central']['isolate'][i] +
    x_scan_central[i] * data['processing_times']['central']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['central_max_hours']

problem += pulp.lpSum([
    x_isolate_distributed[i] * data['processing_times']['distributed']['isolate'][i] +
    x_scan_distributed[i] * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')