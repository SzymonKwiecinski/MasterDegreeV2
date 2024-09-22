import pulp
import json

# Define the data in JSON format
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Extract the data
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Network_Interventions", pulp.LpMinimize)

# Decision Variables
x_isolate_central = pulp.LpVariable.dicts("isolate_central", range(N), cat='Binary')
x_scan_central = pulp.LpVariable.dicts("scan_central", range(N), cat='Binary')
x_isolate_distributed = pulp.LpVariable.dicts("isolate_distributed", range(N), cat='Binary')
x_scan_distributed = pulp.LpVariable.dicts("scan_distributed", range(N), cat='Binary')

# Objective Function
total_cost = pulp.lpSum([
    isolate_central[i] * x_isolate_central[i] * central_cost +
    scan_central[i] * x_scan_central[i] * central_cost +
    isolate_distributed[i] * x_isolate_distributed[i] * distributed_cost +
    scan_distributed[i] * x_scan_distributed[i] * distributed_cost
    for i in range(N)
])
problem += total_cost

# Constraints
# Each cluster must have exactly one intervention type and one processing method
for i in range(N):
    problem += (x_isolate_central[i] + x_scan_central[i] + x_isolate_distributed[i] + x_scan_distributed[i] == 1)

# Central processing time constraint
problem += (pulp.lpSum(isolate_central[i] * x_isolate_central[i] + scan_central[i] * x_scan_central[i] for i in range(N)) <= max_central)

# Distributed processing time constraint
problem += (pulp.lpSum(isolate_distributed[i] * x_isolate_distributed[i] + scan_distributed[i] * x_scan_distributed[i] for i in range(N)) <= max_distributed)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')