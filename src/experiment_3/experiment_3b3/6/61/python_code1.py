import pulp

# Data from JSON
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extract parameters
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Initialize problem
problem = pulp.LpProblem("Minimize Total Costs", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(N)]
y_c = [pulp.LpVariable(f"y_c_{i}", cat='Binary') for i in range(N)]
amount = [pulp.LpVariable(f"amount_{i}", lowBound=0) for i in range(N)]  # Not used in the cost or constraints

# Objective function
problem += pulp.lpSum(
    central_cost * (
        isolate_central[i] * x[i] * y_c[i] + 
        scan_central[i] * (1 - x[i]) * y_c[i]
    ) + 
    distributed_cost * (
        isolate_distributed[i] * x[i] * (1 - y_c[i]) + 
        scan_distributed[i] * (1 - x[i]) * (1 - y_c[i])
    ) 
    for i in range(N)
)

# Constraints
# Central processing time constraint
problem += pulp.lpSum(
    (isolate_central[i] * x[i] + scan_central[i] * (1 - x[i])) * y_c[i]
    for i in range(N)
) <= max_central

# Distributed processing time constraint
problem += pulp.lpSum(
    (isolate_distributed[i] * x[i] + scan_distributed[i] * (1 - x[i])) * (1 - y_c[i])
    for i in range(N)
) <= max_distributed

# Solve the problem
problem.solve()

# Extract results
interventions = []
for i in range(N):
    intervention_type = "isolate" if pulp.value(x[i]) == 1 else "scan"
    method_type = "central" if pulp.value(y_c[i]) == 1 else "distributed"
    interventions.append({
        "cluster_id": i,
        "type": intervention_type,
        "method": method_type,
        "amount": pulp.value(amount[i])  # Not needed in the objective or constraints; shown as part of the output format
    })

output = {
    "interventions": interventions,
    "total_cost": pulp.value(problem.objective)
}

# Print the output for total cost
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')