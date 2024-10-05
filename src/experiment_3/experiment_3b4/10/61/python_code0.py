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

# Extract data
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central_hours = data['max_hours']['central_max_hours']
max_distributed_hours = data['max_hours']['distributed_max_hours']

n = len(isolate_central)  # Number of clusters

# LP Problem
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Decision Variables
x_isolate_central = [pulp.LpVariable(f"x_isolate_central_{i}", cat='Binary') for i in range(n)]
x_scan_central = [pulp.LpVariable(f"x_scan_central_{i}", cat='Binary') for i in range(n)]
x_isolate_distributed = [pulp.LpVariable(f"x_isolate_distributed_{i}", cat='Binary') for i in range(n)]
x_scan_distributed = [pulp.LpVariable(f"x_scan_distributed_{i}", cat='Binary') for i in range(n)]

# Objective Function
problem += pulp.lpSum([
    central_cost * (isolate_central[i] * x_isolate_central[i] + scan_central[i] * x_scan_central[i]) +
    distributed_cost * (isolate_distributed[i] * x_isolate_distributed[i] + scan_distributed[i] * x_scan_distributed[i])
    for i in range(n)
])

# Constraints
# Each cluster must be treated with one type of intervention
for i in range(n):
    problem += (x_isolate_central[i] + x_scan_central[i] + x_isolate_distributed[i] + x_scan_distributed[i] == 1, f"unique_intervention_{i}")

# Total central processing time constraint
problem += pulp.lpSum([
    isolate_central[i] * x_isolate_central[i] + scan_central[i] * x_scan_central[i]
    for i in range(n)
]) <= max_central_hours, "central_time_constraint"

# Total distributed processing time constraint
problem += pulp.lpSum([
    isolate_distributed[i] * x_isolate_distributed[i] + scan_distributed[i] * x_scan_distributed[i]
    for i in range(n)
]) <= max_distributed_hours, "distributed_time_constraint"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')