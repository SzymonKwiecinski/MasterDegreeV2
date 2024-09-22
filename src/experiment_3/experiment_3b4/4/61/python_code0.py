import pulp

# Data from the JSON
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
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(isolate_central)  # Number of clusters

# Create the MILP model
problem = pulp.LpProblem("NetworkIntrusionIntervention", pulp.LpMinimize)

# Decision variables
x_c_iso = [pulp.LpVariable(f'x_{i}_c_iso', cat='Binary') for i in range(N)]
x_c_scan = [pulp.LpVariable(f'x_{i}_c_scan', cat='Binary') for i in range(N)]
x_d_iso = [pulp.LpVariable(f'x_{i}_d_iso', cat='Binary') for i in range(N)]
x_d_scan = [pulp.LpVariable(f'x_{i}_d_scan', cat='Binary') for i in range(N)]

# Objective function
problem += pulp.lpSum(
    central_cost * (isolate_central[i] * x_c_iso[i] + scan_central[i] * x_c_scan[i]) +
    distributed_cost * (isolate_distributed[i] * x_d_iso[i] + scan_distributed[i] * x_d_scan[i])
    for i in range(N)
)

# Constraints
# Central Processing Time Constraint
problem += pulp.lpSum(isolate_central[i] * x_c_iso[i] + scan_central[i] * x_c_scan[i] for i in range(N)) <= max_central

# Distributed Processing Time Constraint
problem += pulp.lpSum(isolate_distributed[i] * x_d_iso[i] + scan_distributed[i] * x_d_scan[i] for i in range(N)) <= max_distributed

# One Intervention per Cluster Constraint
for i in range(N):
    problem += x_c_iso[i] + x_c_scan[i] + x_d_iso[i] + x_d_scan[i] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')