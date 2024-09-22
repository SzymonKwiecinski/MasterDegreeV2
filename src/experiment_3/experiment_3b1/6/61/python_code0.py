import pulp

# Data from the JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting parameters from the data
N = len(data['processing_times']['central']['isolate'])

isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), cat='Binary')

# Objective function
problem += pulp.lpSum([
    x[i, 'isolate', 'central'] * isolate_central[i] * central_cost +
    x[i, 'scan', 'central'] * scan_central[i] * central_cost +
    x[i, 'isolate', 'distributed'] * isolate_distributed[i] * distributed_cost +
    x[i, 'scan', 'distributed'] * scan_distributed[i] * distributed_cost
    for i in range(N)
]), "Total_Cost"

# Constraints
# Each cluster can only have one type of intervention consistently
for i in range(N):
    problem += pulp.lpSum([x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']]) == 1, f"One_intervention_{i}"

# Maximum hours for central processing
problem += pulp.lpSum([
    x[i, 'isolate', 'central'] * isolate_central[i] +
    x[i, 'scan', 'central'] * scan_central[i]
    for i in range(N)
]) <= max_central, "Max_Central_Hours"

# Maximum hours for distributed processing
problem += pulp.lpSum([
    x[i, 'isolate', 'distributed'] * isolate_distributed[i] +
    x[i, 'scan', 'distributed'] * scan_distributed[i]
    for i in range(N)
]) <= max_distributed, "Max_Distributed_Hours"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')