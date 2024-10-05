import pulp

# Extract data from JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Set the number of clusters
N = len(data['processing_times']['central']['isolate'])

# Initialize the LP problem
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Decision variables
x_isolate = [pulp.LpVariable(f"x_isolate_{i}", cat='Binary') for i in range(N)]
x_scan = [pulp.LpVariable(f"x_scan_{i}", cat='Binary') for i in range(N)]

# Objective function
problem += pulp.lpSum([
    data['costs']['central'] * x_isolate[i] * data['processing_times']['central']['isolate'][i] +
    data['costs']['central'] * x_scan[i] * data['processing_times']['central']['scan'][i] +
    data['costs']['distributed'] * (1 - x_isolate[i]) * data['processing_times']['distributed']['isolate'][i] +
    data['costs']['distributed'] * (1 - x_scan[i]) * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
])

# Constraints
# Time constraints for central processing
problem += pulp.lpSum([
    x_isolate[i] * data['processing_times']['central']['isolate'][i] +
    x_scan[i] * data['processing_times']['central']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['central_max_hours']

# Time constraints for distributed processing
problem += pulp.lpSum([
    (1 - x_isolate[i]) * data['processing_times']['distributed']['isolate'][i] +
    (1 - x_scan[i]) * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['distributed_max_hours']

# Each cluster must have exactly one intervention type
for i in range(N):
    problem += x_isolate[i] + x_scan[i] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the interventions
interventions = []
for i in range(N):
    intervention_type = "isolate" if x_isolate[i].varValue == 1 else "scan"
    method = "central" if (x_isolate[i].varValue == 1 and data['processing_times']['central']['isolate'][i] < data['processing_times']['distributed']['isolate'][i]) or \
                         (x_scan[i].varValue == 1 and data['processing_times']['central']['scan'][i] < data['processing_times']['distributed']['scan'][i]) else "distributed"
    interventions.append({
        "cluster_id": i,
        "type": intervention_type,
        "method": method,
        "amount": 1
    })

# Print interventions
for intervention in interventions:
    print(intervention)