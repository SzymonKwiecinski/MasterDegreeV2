import pulp

# Data from the input
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

# Input data
processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(processing_times['central']['isolate'])  # Number of clusters

# Define the MILP problem
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
x_central_isolate = [pulp.LpVariable(f"x_central_isolate_{i}", 0, None, pulp.LpContinuous) for i in range(N)]
x_central_scan = [pulp.LpVariable(f"x_central_scan_{i}", 0, None, pulp.LpContinuous) for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f"x_distributed_isolate_{i}", 0, None, pulp.LpContinuous) for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f"x_distributed_scan_{i}", 0, None, pulp.LpContinuous) for i in range(N)]

# Objective function
problem += pulp.lpSum(
    central_cost * (x_central_isolate[i] + x_central_scan[i]) +
    distributed_cost * (x_distributed_isolate[i] + x_distributed_scan[i])
    for i in range(N)
)

# Constraints
# Central and distributed maximum hours
problem += pulp.lpSum(processing_times['central']['isolate'][i] * x_central_isolate[i] + 
                      processing_times['central']['scan'][i] * x_central_scan[i]
                      for i in range(N)) <= max_central, "Central_Max_Hours"

problem += pulp.lpSum(processing_times['distributed']['isolate'][i] * x_distributed_isolate[i] + 
                      processing_times['distributed']['scan'][i] * x_distributed_scan[i]
                      for i in range(N)) <= max_distributed, "Distributed_Max_Hours"

# Each cluster must pick one intervention type and method
for i in range(N):
    problem += (x_central_isolate[i] + x_central_scan[i] + 
                x_distributed_isolate[i] + x_distributed_scan[i] == 1), f"Cluster_{i+1}_Intervention_Choice"

# Solve the problem
problem.solve()

# Collect and format results
interventions = []
for i in range(N):
    if pulp.value(x_central_isolate[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": pulp.value(x_central_isolate[i])})
    elif pulp.value(x_central_scan[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": pulp.value(x_central_scan[i])})
    elif pulp.value(x_distributed_isolate[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": pulp.value(x_distributed_isolate[i])})
    elif pulp.value(x_distributed_scan[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": pulp.value(x_distributed_scan[i])})

total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')