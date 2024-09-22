import pulp
import json

# Load data from JSON format
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Extract the data from the loaded JSON
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
C_c = data['costs']['central']
C_d = data['costs']['distributed']
H_c = data['max_hours']['central_max_hours']
H_d = data['max_hours']['distributed_max_hours']
N = len(isolate_central)  # Total number of clusters

# Initialize the problem
problem = pulp.LpProblem("Network_Intervention_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
    ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), 
    cat='Binary')

# Objective function
problem += pulp.lpSum(
    C_c * isolate_central[i] * x[(i, 'isolate', 'central')] +
    C_c * scan_central[i] * x[(i, 'scan', 'central')] +
    C_d * isolate_distributed[i] * x[(i, 'isolate', 'distributed')] +
    C_d * scan_distributed[i] * x[(i, 'scan', 'distributed')]
    for i in range(N)
), "Total Cost"

# Constraints
# Intervention type consistency
for i in range(N):
    problem += pulp.lpSum(x[(i, j, k)] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1, f"InterventionConsistency_{i}"

# Maximum hours for central processing
problem += pulp.lpSum(
    isolate_central[i] * x[(i, 'isolate', 'central')] +
    scan_central[i] * x[(i, 'scan', 'central')]
    for i in range(N)
) <= H_c, "MaxCentralHours"

# Maximum hours for distributed processing
problem += pulp.lpSum(
    isolate_distributed[i] * x[(i, 'isolate', 'distributed')] +
    scan_distributed[i] * x[(i, 'scan', 'distributed')]
    for i in range(N)
) <= H_d, "MaxDistributedHours"

# Solve the problem
problem.solve()

# Print the results
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(x[(i, j, k)]) == 1:
                print(f'Cluster {i+1}: Intervention Type: {j}, Processing Method: {k}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')