from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, value
import json

# Load the data
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Extract the data
N = len(data['processing_times']['central']['isolate'])
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = LpProblem("IntrusionIntervention", LpMinimize)

# Decision variables
x_central_isolate = [LpVariable(f"x_central_isolate_{i}", 0, 1, LpBinary) for i in range(N)]
x_central_scan = [LpVariable(f"x_central_scan_{i}", 0, 1, LpBinary) for i in range(N)]
x_distributed_isolate = [LpVariable(f"x_distributed_isolate_{i}", 0, 1, LpBinary) for i in range(N)]
x_distributed_scan = [LpVariable(f"x_distributed_scan_{i}", 0, 1, LpBinary) for i in range(N)]

# Objective function
total_cost = lpSum([
    x_central_isolate[i] * central_isolate[i] * central_cost +
    x_central_scan[i] * central_scan[i] * central_cost +
    x_distributed_isolate[i] * distributed_isolate[i] * distributed_cost +
    x_distributed_scan[i] * distributed_scan[i] * distributed_cost
    for i in range(N)
])
problem += total_cost

# Constraints
# Each cluster must have exactly one intervention
for i in range(N):
    problem += (x_central_isolate[i] + x_central_scan[i] + x_distributed_isolate[i] + x_distributed_scan[i] == 1)
    
# Central processing time constraints
problem += lpSum([x_central_isolate[i] * central_isolate[i] + x_central_scan[i] * central_scan[i] for i in range(N)]) <= max_central

# Distributed processing time constraints
problem += lpSum([x_distributed_isolate[i] * distributed_isolate[i] + x_distributed_scan[i] * distributed_scan[i] for i in range(N)]) <= max_distributed

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in range(N):
    if value(x_central_isolate[i]):
        interventions.append({
            "cluster_id": i+1,
            "type": "isolate",
            "method": "central",
            "amount": value(x_central_isolate[i])
        })
    elif value(x_central_scan[i]):
        interventions.append({
            "cluster_id": i+1,
            "type": "scan",
            "method": "central",
            "amount": value(x_central_scan[i])
        })
    elif value(x_distributed_isolate[i]):
        interventions.append({
            "cluster_id": i+1,
            "type": "isolate",
            "method": "distributed",
            "amount": value(x_distributed_isolate[i])
        })
    else:  # x_distributed_scan must be 1
        interventions.append({
            "cluster_id": i+1,
            "type": "scan",
            "method": "distributed",
            "amount": value(x_distributed_scan[i])
        })

# Output results
output = {
    "interventions": interventions,
    "total_cost": value(total_cost)
}

print(json.dumps(output, indent=4))

# Print objective
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')