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

# Create a problem instance
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Extract data
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Number of clusters
N = len(central_isolate)

# Decision variables
intervention_central_isolate = [pulp.LpVariable(f"central_isolate_{i}", cat='Binary') for i in range(N)]
intervention_central_scan = [pulp.LpVariable(f"central_scan_{i}", cat='Binary') for i in range(N)]
intervention_distributed_isolate = [pulp.LpVariable(f"distributed_isolate_{i}", cat='Binary') for i in range(N)]
intervention_distributed_scan = [pulp.LpVariable(f"distributed_scan_{i}", cat='Binary') for i in range(N)]

# Objective function: Minimize total cost
problem += pulp.lpSum([
    central_cost * (central_isolate[i] * intervention_central_isolate[i] +
                    central_scan[i] * intervention_central_scan[i]) +
    distributed_cost * (distributed_isolate[i] * intervention_distributed_isolate[i] +
                        distributed_scan[i] * intervention_distributed_scan[i])
    for i in range(N)
])

# Constraint: Each cluster must choose exactly one intervention type and method
for i in range(N):
    problem += (intervention_central_isolate[i] + 
                intervention_central_scan[i] + 
                intervention_distributed_isolate[i] +
                intervention_distributed_scan[i] == 1)

# Constraint: Central processing time
problem += pulp.lpSum([
    central_isolate[i] * intervention_central_isolate[i] + 
    central_scan[i] * intervention_central_scan[i]
    for i in range(N)
]) <= max_central

# Constraint: Distributed processing time
problem += pulp.lpSum([
    distributed_isolate[i] * intervention_distributed_isolate[i] + 
    distributed_scan[i] * intervention_distributed_scan[i]
    for i in range(N)
]) <= max_distributed

# Solve the problem
problem.solve()

# Output
interventions = [
    {
        "cluster_id": i,
        "type": ("isolate" if intervention_central_isolate[i].value() or intervention_distributed_isolate[i].value() else "scan"),
        "method": ("central" if intervention_central_isolate[i].value() or intervention_central_scan[i].value() else "distributed"),
        "amount": central_isolate[i] if intervention_central_isolate[i].value() else
                  (central_scan[i] if intervention_central_scan[i].value() else
                   (distributed_isolate[i] if intervention_distributed_isolate[i].value() else distributed_scan[i]))
    }
    for i in range(N)
]

total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')