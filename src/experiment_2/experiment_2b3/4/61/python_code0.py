import pulp

# Data from input
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting data
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(central_isolate)

# Problem definition
problem = pulp.LpProblem("Network_Intervention_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("central_isolate", (i for i in range(N)), cat=pulp.LpBinary)
y = pulp.LpVariable.dicts("central_scan", (i for i in range(N)), cat=pulp.LpBinary)
z = pulp.LpVariable.dicts("distributed_isolate", (i for i in range(N)), cat=pulp.LpBinary)
w = pulp.LpVariable.dicts("distributed_scan", (i for i in range(N)), cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum([
    central_cost * (x[i] * central_isolate[i] + y[i] * central_scan[i]) +
    distributed_cost * (z[i] * distributed_isolate[i] + w[i] * distributed_scan[i])
    for i in range(N)
])

# Constraints
# Each cluster must be treated with one intervention type
for i in range(N):
    problem += x[i] + y[i] + z[i] + w[i] == 1

# Maximum hour constraints for central processing
problem += pulp.lpSum([x[i] * central_isolate[i] + y[i] * central_scan[i] for i in range(N)]) <= max_central

# Maximum hour constraints for distributed processing
problem += pulp.lpSum([z[i] * distributed_isolate[i] + w[i] * distributed_scan[i] for i in range(N)]) <= max_distributed

# Solve the problem
problem.solve()

# Output the results
interventions = []
total_cost = pulp.value(problem.objective)

for i in range(N):
    if pulp.value(x[i]) == 1:
        interventions.append({"cluster_id": i + 1, "type": "isolate", "method": "central", "amount": central_isolate[i]})
    elif pulp.value(y[i]) == 1:
        interventions.append({"cluster_id": i + 1, "type": "scan", "method": "central", "amount": central_scan[i]})
    elif pulp.value(z[i]) == 1:
        interventions.append({"cluster_id": i + 1, "type": "isolate", "method": "distributed", "amount": distributed_isolate[i]})
    elif pulp.value(w[i]) == 1:
        interventions.append({"cluster_id": i + 1, "type": "scan", "method": "distributed", "amount": distributed_scan[i]})

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')