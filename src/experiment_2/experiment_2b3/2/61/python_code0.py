import pulp

data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extract the data
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

central_cost = costs['central']
distributed_cost = costs['distributed']
max_central = max_hours['central_max_hours']
max_distributed = max_hours['distributed_max_hours']

N = len(processing_times['central']['isolate'])

# Define the problem
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Variables
intervention_vars = pulp.LpVariable.dicts(
    "Intervention",
    ((i, itype, method) for i in range(N) for itype in ['isolate', 'scan'] for method in ['central', 'distributed']),
    cat='Binary'
)

# Objective function: Minimize the total cost
problem += pulp.lpSum([
    intervention_vars[(i, 'isolate', 'central')] * processing_times['central']['isolate'][i] * central_cost +
    intervention_vars[(i, 'scan', 'central')] * processing_times['central']['scan'][i] * central_cost +
    intervention_vars[(i, 'isolate', 'distributed')] * processing_times['distributed']['isolate'][i] * distributed_cost +
    intervention_vars[(i, 'scan', 'distributed')] * processing_times['distributed']['scan'][i] * distributed_cost
    for i in range(N)
])

# Constraints: Each cluster must receive exactly one type of intervention
for i in range(N):
    problem += (
        intervention_vars[(i, 'isolate', 'central')] +
        intervention_vars[(i, 'scan', 'central')] +
        intervention_vars[(i, 'isolate', 'distributed')] +
        intervention_vars[(i, 'scan', 'distributed')] == 1
    )

# Central processing time limit
problem += pulp.lpSum([
    intervention_vars[(i, 'isolate', 'central')] * processing_times['central']['isolate'][i] +
    intervention_vars[(i, 'scan', 'central')] * processing_times['central']['scan'][i]
    for i in range(N)
]) <= max_central

# Distributed processing time limit
problem += pulp.lpSum([
    intervention_vars[(i, 'isolate', 'distributed')] * processing_times['distributed']['isolate'][i] +
    intervention_vars[(i, 'scan', 'distributed')] * processing_times['distributed']['scan'][i]
    for i in range(N)
]) <= max_distributed

# Solve the problem
problem.solve()

output = {
    "interventions": [],
    "total_cost": pulp.value(problem.objective)
}

# Gather results
for i in range(N):
    for itype in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(intervention_vars[(i, itype, method)]) == 1:
                output["interventions"].append({
                    "cluster_id": i,
                    "type": itype,
                    "method": method,
                    "amount": 1  # always 1 as it's binary
                })

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')