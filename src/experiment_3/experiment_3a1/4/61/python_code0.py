import pulp
import json

# Load data from JSON format
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Extracting data from JSON
clusters = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Network_Intrusion_Interventions", pulp.LpMinimize)

# Decision Variables
x_isolate = [pulp.LpVariable(f'x_{i+1}_isolate', cat='Binary') for i in range(clusters)]
x_scan = [pulp.LpVariable(f'x_{i+1}_scan', cat='Binary') for i in range(clusters)]
y_central = [pulp.LpVariable(f'y_{i+1}_central', cat='Binary') for i in range(clusters)]
y_distributed = [pulp.LpVariable(f'y_{i+1}_distributed', cat='Binary') for i in range(clusters)]

# Objective function
Z = pulp.lpSum([
    (isolate_central[i] * y_central[i] + scan_central[i] * y_central[i] +
     isolate_distributed[i] * y_distributed[i] + scan_distributed[i] * y_distributed[i]) *
    (central_cost * y_central[i] + distributed_cost * y_distributed[i])
    for i in range(clusters)
])
problem += Z

# Constraints
# Cluster Intervention Consistency
for i in range(clusters):
    problem += (x_isolate[i] + x_scan[i] == 1)

# Central Processing Time Constraint
problem += (pulp.lpSum(isolate_central[i] * y_central[i] + scan_central[i] * y_central[i] for i in range(clusters)) <= max_central)

# Distributed Processing Time Constraint
problem += (pulp.lpSum(isolate_distributed[i] * y_distributed[i] + scan_distributed[i] * y_distributed[i] for i in range(clusters)) <= max_distributed)

# Intervention Type Selection
for i in range(clusters):
    problem += (x_isolate[i] * y_central[i] + x_isolate[i] * y_distributed[i] == x_isolate[i])
    problem += (x_scan[i] * y_central[i] + x_scan[i] * y_distributed[i] == x_scan[i])

# Solve the problem
problem.solve()

# Output result
results = []
for i in range(clusters):
    if pulp.value(x_isolate[i]) == 1:
        intervention_type = "isolate"
    else:
        intervention_type = "scan"
    
    if pulp.value(y_central[i]) == 1:
        method = "central"
    elif pulp.value(y_distributed[i]) == 1:
        method = "distributed"
    else:
        method = "none"
    
    amount = (isolate_central[i] if intervention_type == "isolate" and method == "central" else
              scan_central[i] if intervention_type == "scan" and method == "central" else
              isolate_distributed[i] if intervention_type == "isolate" and method == "distributed" else
              scan_distributed[i] if intervention_type == "scan" and method == "distributed" else 0)

    results.append({
        "cluster_id": i + 1,
        "type": intervention_type,
        "method": method,
        "amount": amount
    })

# Print results and the objective value
for result in results:
    print(result)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')