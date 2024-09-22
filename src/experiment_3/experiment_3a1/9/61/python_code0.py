import pulp
import json

# Data provided in JSON format
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

# Extract data
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create a LP problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in ['isolate', 'scan']), cat='Binary')
y = pulp.LpVariable.dicts("y", ((i, k) for i in range(N) for k in ['central', 'distributed']), cat='Binary')

# Objective function
problem += pulp.lpSum(
    (central_cost * x[i, 'isolate'] * y[i, 'central'] * isolate_central[i] +
     central_cost * x[i, 'scan'] * y[i, 'central'] * scan_central[i] +
     distributed_cost * x[i, 'isolate'] * y[i, 'distributed'] * isolate_distributed[i] +
     distributed_cost * x[i, 'scan'] * y[i, 'distributed'] * scan_distributed[i])
    for i in range(N)
), "Total Cost"

# Constraints

# Each cluster must have exactly one intervention type
for i in range(N):
    problem += x[i, 'isolate'] + x[i, 'scan'] == 1, f"One_Intervention_Type_{i}"

# Total processing time for central interventions must not exceed maximum hours
problem += pulp.lpSum(
    isolate_central[i] * x[i, 'isolate'] + scan_central[i] * x[i, 'scan'] for i in range(N)
) <= max_central, "Max_Central_Processing_Time"

# Total processing time for distributed interventions must not exceed maximum hours
problem += pulp.lpSum(
    isolate_distributed[i] * x[i, 'isolate'] + scan_distributed[i] * x[i, 'scan'] for i in range(N)
) <= max_distributed, "Max_Distributed_Processing_Time"

# Ensure that a chosen intervention method matches the processing type
for i in range(N):
    problem += x[i, 'isolate'] + x[i, 'scan'] == 1, f"Intervention_Type_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')