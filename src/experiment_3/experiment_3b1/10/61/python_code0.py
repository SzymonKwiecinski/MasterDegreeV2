import pulp
import json

# Data parsed from JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
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

# Extracting parameters from the data
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Creating the problem
problem = pulp.LpProblem("MILP_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']), cat='Binary')

# Objective Function
problem += pulp.lpSum((
    isolate_central[i] * central_cost * x[i]['isolate_central'] +
    scan_central[i] * central_cost * x[i]['scan_central'] +
    isolate_distributed[i] * distributed_cost * x[i]['isolate_distributed'] +
    scan_distributed[i] * distributed_cost * x[i]['scan_distributed']
) for i in range(N)), "Total_Cost"

# Constraints
# Each cluster must have exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']) == 1, f"One_Intervention_Cluster_{i}"

# Central processing time limit
problem += pulp.lpSum(
    (isolate_central[i] * x[i]['isolate_central'] + scan_central[i] * x[i]['scan_central']) for i in range(N)
) <= max_central, "Central_Time_Limit"

# Distributed processing time limit
problem += pulp.lpSum(
    (isolate_distributed[i] * x[i]['isolate_distributed'] + scan_distributed[i] * x[i]['scan_distributed']) for i in range(N)
) <= max_distributed, "Distributed_Time_Limit"

# Solve the problem
problem.solve()

# Print results
print("Interventions:")
for i in range(N):
    for j in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']:
        if pulp.value(x[i][j]) == 1:
            print(f"Cluster {i+1}: {j}")

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')