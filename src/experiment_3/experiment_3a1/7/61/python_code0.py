import pulp

# Data from the provided JSON format
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

# Extracting the data
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']
N = len(isolate_central)

# Create the problem
problem = pulp.LpProblem("Intrusion_Intervention_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')  # Intervention type: isolate (1) or scan (0)
y_central = pulp.LpVariable.dicts("y_central", range(N), cat='Binary')  # Central processing indicator
y_distributed = pulp.LpVariable.dicts("y_distributed", range(N), cat='Binary')  # Distributed processing indicator

# Objective function
total_cost = pulp.lpSum([
    x[i] * y_central[i] * central_cost * isolate_central[i] +
    x[i] * y_distributed[i] * distributed_cost * isolate_distributed[i] +
    (1 - x[i]) * y_central[i] * central_cost * scan_central[i] +
    (1 - x[i]) * y_distributed[i] * distributed_cost * scan_distributed[i]
    for i in range(N)
])
problem += total_cost

# Constraints
# Each cluster must have exactly one intervention processed
for i in range(N):
    problem += (y_central[i] + y_distributed[i] == 1)

# Total processing time for central processing must not exceed the maximum hours
problem += (pulp.lpSum([
    x[i] * isolate_central[i] * y_central[i] +
    (1 - x[i]) * scan_central[i] * y_central[i] 
    for i in range(N)
]) <= max_central)

# Total processing time for distributed processing must not exceed the maximum hours
problem += (pulp.lpSum([
    x[i] * isolate_distributed[i] * y_distributed[i] +
    (1 - x[i]) * scan_distributed[i] * y_distributed[i] 
    for i in range(N)
]) <= max_distributed)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')