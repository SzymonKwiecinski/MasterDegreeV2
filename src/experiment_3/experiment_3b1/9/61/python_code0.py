import pulp
import json

# Data provided in JSON format
data = '''{
    "processing_times": {
        "central": {
            "isolate": [10, 6, 8],
            "scan": [6, 4, 6]
        },
        "distributed": {
            "isolate": [12, 9, 12],
            "scan": [18, 10, 15]
        }
    },
    "costs": {
        "central": 150,
        "distributed": 70
    },
    "max_hours": {
        "central_max_hours": 16,
        "distributed_max_hours": 33
    }
}'''

# Load data
data = json.loads(data)

# Parameters
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Decision Variables
x_isolate_central = [pulp.LpVariable(f'x_isolate_central_{i}', cat='Binary') for i in range(N)]
x_scan_central = [pulp.LpVariable(f'x_scan_central_{i}', cat='Binary') for i in range(N)]
x_isolate_distributed = [pulp.LpVariable(f'x_isolate_distributed_{i}', cat='Binary') for i in range(N)]
x_scan_distributed = [pulp.LpVariable(f'x_scan_distributed_{i}', cat='Binary') for i in range(N)]

# Problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Objective Function
total_cost = pulp.lpSum([
    central_cost * (isolate_central[i] * x_isolate_central[i] + scan_central[i] * x_scan_central[i]) +
    distributed_cost * (isolate_distributed[i] * x_isolate_distributed[i] + scan_distributed[i] * x_scan_distributed[i])
    for i in range(N)
])
problem += total_cost

# Constraints
# Each cluster must have exactly one type of intervention
for i in range(N):
    problem += (x_isolate_central[i] + x_scan_central[i] + x_isolate_distributed[i] + x_scan_distributed[i] == 1)

# Central processing time constraint
problem += (pulp.lpSum(isolate_central[i] * x_isolate_central[i] + scan_central[i] * x_scan_central[i] for i in range(N)) <= max_central)

# Distributed processing time constraint
problem += (pulp.lpSum(isolate_distributed[i] * x_isolate_distributed[i] + scan_distributed[i] * x_scan_distributed[i] for i in range(N)) <= max_distributed)

# Solve the problem
problem.solve()

# Output the selected interventions and total cost
interventions = []
for i in range(N):
    if pulp.value(x_isolate_central[i]) == 1:
        interventions.append(f'(cluster_id = {i+1}, type = "isolate", method = "central")')
    elif pulp.value(x_scan_central[i]) == 1:
        interventions.append(f'(cluster_id = {i+1}, type = "scan", method = "central")')
    elif pulp.value(x_isolate_distributed[i]) == 1:
        interventions.append(f'(cluster_id = {i+1}, type = "isolate", method = "distributed")')
    elif pulp.value(x_scan_distributed[i]) == 1:
        interventions.append(f'(cluster_id = {i+1}, type = "scan", method = "distributed")')

print(f'Interventions: {interventions}')
print(f'Total Cost: <OBJ>{pulp.value(problem.objective)}</OBJ>')