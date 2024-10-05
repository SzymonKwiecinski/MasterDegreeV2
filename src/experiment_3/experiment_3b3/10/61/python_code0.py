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

# Number of clusters
N = len(data['processing_times']['central']['isolate'])

# Parameters
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Creating the Linear Programming Problem
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Decision Variables
x_isolate_central = [pulp.LpVariable(f'x_isolate_central_{i}', lowBound=0) for i in range(N)]
x_scan_central = [pulp.LpVariable(f'x_scan_central_{i}', lowBound=0) for i in range(N)]
x_isolate_distributed = [pulp.LpVariable(f'x_isolate_distributed_{i}', lowBound=0) for i in range(N)]
x_scan_distributed = [pulp.LpVariable(f'x_scan_distributed_{i}', lowBound=0) for i in range(N)]

# Objective Function
problem += pulp.lpSum([
    central_cost * (x_isolate_central[i] + x_scan_central[i]) +
    distributed_cost * (x_isolate_distributed[i] + x_scan_distributed[i])
    for i in range(N)
]), "Total_Cost"

# Constraints
problem += pulp.lpSum([
    x_isolate_central[i] + x_scan_central[i]
    for i in range(N)
]) <= max_central, "Central_Processing_Time_Constraint"

problem += pulp.lpSum([
    x_isolate_distributed[i] + x_scan_distributed[i]
    for i in range(N)
]) <= max_distributed, "Distributed_Processing_Time_Constraint"

# Required intervention assumed to be the sum of all possible interventions.
# This is a derived constraint based on provided times.
required_intervention = [isolate_central[i] + scan_central[i] + isolate_distributed[i] + scan_distributed[i] for i in range(N)]

for i in range(N):
    problem += (
        x_isolate_central[i] + x_scan_central[i] +
        x_isolate_distributed[i] + x_scan_distributed[i]
        >= required_intervention[i], f"Required_Intervention_Cluster_{i}"
    )

# Solve the problem
problem.solve()

# Output results
for i in range(N):
    print(f"Cluster {i}:")
    print(f"  Central Isolate: {x_isolate_central[i].varValue}")
    print(f"  Central Scan: {x_scan_central[i].varValue}")
    print(f"  Distributed Isolate: {x_isolate_distributed[i].varValue}")
    print(f"  Distributed Scan: {x_scan_distributed[i].varValue}")

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")