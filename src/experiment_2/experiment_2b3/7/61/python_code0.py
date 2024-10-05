import pulp

# Parse the input data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

# Number of clusters
N = len(processing_times['central']['isolate'])

# Create the problem instance
problem = pulp.LpProblem("Network_Intervention_Optimization", pulp.LpMinimize)

# Decision Variables
x_central_isolate = [pulp.LpVariable(f"x_central_isolate_{i}", lowBound=0, cat='Continuous') for i in range(N)]
x_central_scan = [pulp.LpVariable(f"x_central_scan_{i}", lowBound=0, cat='Continuous') for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f"x_distributed_isolate_{i}", lowBound=0, cat='Continuous') for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f"x_distributed_scan_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
total_cost = (
    pulp.lpSum(costs['central'] * (x_central_isolate[i] * processing_times['central']['isolate'][i] +
                                   x_central_scan[i] * processing_times['central']['scan'][i]) for i in range(N)) +
    pulp.lpSum(costs['distributed'] * (x_distributed_isolate[i] * processing_times['distributed']['isolate'][i] +
                                       x_distributed_scan[i] * processing_times['distributed']['scan'][i]) for i in range(N))
)

problem += total_cost

# Constraints
# Each cluster must have only one type of intervention
for i in range(N):
    problem += x_central_isolate[i] + x_central_scan[i] + x_distributed_isolate[i] + x_distributed_scan[i] == 1

# Maximum hours constraints for central and distributed processing
problem += pulp.lpSum(x_central_isolate[i] * processing_times['central']['isolate'][i] +
                      x_central_scan[i] * processing_times['central']['scan'][i] for i in range(N)) <= max_hours['central_max_hours']

problem += pulp.lpSum(x_distributed_isolate[i] * processing_times['distributed']['isolate'][i] +
                      x_distributed_scan[i] * processing_times['distributed']['scan'][i] for i in range(N)) <= max_hours['distributed_max_hours']

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in range(N):
    if pulp.value(x_central_isolate[i]) > 0.5:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": pulp.value(x_central_isolate[i])})
    elif pulp.value(x_central_scan[i]) > 0.5:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": pulp.value(x_central_scan[i])})
    elif pulp.value(x_distributed_isolate[i]) > 0.5:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": pulp.value(x_distributed_isolate[i])})
    elif pulp.value(x_distributed_scan[i]) > 0.5:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": pulp.value(x_distributed_scan[i])})

total_cost_value = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')