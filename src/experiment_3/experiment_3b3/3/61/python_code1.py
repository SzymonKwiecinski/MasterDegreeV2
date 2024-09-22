import pulp

# Data provided
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

N = len(data['processing_times']['central']['isolate'])

# Create a problem variable
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x_isolate_central = pulp.LpVariable.dicts("x_isolate_central", range(N), cat='Binary')
x_scan_central = pulp.LpVariable.dicts("x_scan_central", range(N), cat='Binary')
y_isolate_distributed = pulp.LpVariable.dicts("y_isolate_distributed", range(N), cat='Binary')
y_scan_distributed = pulp.LpVariable.dicts("y_scan_distributed", range(N), cat='Binary')

# Objective Function
problem += pulp.lpSum([
    data['processing_times']['central']['isolate'][i] * x_isolate_central[i] * data['costs']['central'] +
    data['processing_times']['central']['scan'][i] * x_scan_central[i] * data['costs']['central'] +
    data['processing_times']['distributed']['isolate'][i] * y_isolate_distributed[i] * data['costs']['distributed'] +
    data['processing_times']['distributed']['scan'][i] * y_scan_distributed[i] * data['costs']['distributed']
    for i in range(N)
])

# Constraints
# Each cluster must have one intervention type consistently
for i in range(N):
    problem += (x_isolate_central[i] + x_scan_central[i] + y_isolate_distributed[i] + y_scan_distributed[i]) == 1

# Central processing time must not exceed maximum hours
problem += pulp.lpSum([
    data['processing_times']['central']['isolate'][i] * x_isolate_central[i] +
    data['processing_times']['central']['scan'][i] * x_scan_central[i]
    for i in range(N)
]) <= data['max_hours']['central_max_hours']

# Distributed processing time must not exceed maximum hours
problem += pulp.lpSum([
    data['processing_times']['distributed']['isolate'][i] * y_isolate_distributed[i] +
    data['processing_times']['distributed']['scan'][i] * y_scan_distributed[i]
    for i in range(N)
]) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output details of the interventions for each cluster
output = []
for i in range(N):
    if x_isolate_central[i].varValue == 1:
        output.append(f"Cluster {i+1}: Isolate Centrally")
    elif x_scan_central[i].varValue == 1:
        output.append(f"Cluster {i+1}: Scan Centrally")
    elif y_isolate_distributed[i].varValue == 1:
        output.append(f"Cluster {i+1}: Isolate Distributed")
    elif y_scan_distributed[i].varValue == 1:
        output.append(f"Cluster {i+1}: Scan Distributed")

print(output)