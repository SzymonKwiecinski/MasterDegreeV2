import pulp

# Data from JSON
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
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']
N = len(processing_times['central']['isolate'])

# Problem definition
problem = pulp.LpProblem("Network_Intrusion_Response", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Intervention",
                          ((i, intervention, method) for i in range(N)
                           for intervention in ['isolate', 'scan']
                           for method in ['central', 'distributed']),
                          cat='Binary')

# Objective function
total_cost = pulp.lpSum([
    costs[method] * processing_times[method][intervention][i] * x[i, intervention, method]
    for i in range(N)
    for intervention in ['isolate', 'scan']
    for method in ['central', 'distributed']
])

problem += total_cost

# Constraints
# Each cluster must be treated with exactly one intervention method
for i in range(N):
    problem += pulp.lpSum([x[i, intervention, method]
                           for intervention in ['isolate', 'scan']
                           for method in ['central', 'distributed']]) == 1

# Central processing time constraint
problem += pulp.lpSum([
    processing_times['central'][intervention][i] * x[i, intervention, 'central']
    for i in range(N)
    for intervention in ['isolate', 'scan']
]) <= max_hours['central_max_hours']

# Distributed processing time constraint
problem += pulp.lpSum([
    processing_times['distributed'][intervention][i] * x[i, intervention, 'distributed']
    for i in range(N)
    for intervention in ['isolate', 'scan']
]) <= max_hours['distributed_max_hours']

# Solve the problem
problem.solve()

# Collect results
interventions_output = []
for i in range(N):
    for intervention in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(x[i, intervention, method]) == 1:
                interventions_output.append({
                    "cluster_id": i,
                    "type": intervention,
                    "method": method,
                    "amount": 1
                })

total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "interventions": interventions_output,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')