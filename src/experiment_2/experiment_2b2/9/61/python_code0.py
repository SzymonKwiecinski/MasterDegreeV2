import pulp

# Data input
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Constants
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Problem definition
problem = pulp.LpProblem("Intrusion_Intervention_Problem", pulp.LpMinimize)

# Decision variables
x_central_isolate = [pulp.LpVariable(f"x_central_isolate_{i}", cat=pulp.LpBinary) for i in range(N)]
x_central_scan = [pulp.LpVariable(f"x_central_scan_{i}", cat=pulp.LpBinary) for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f"x_distributed_isolate_{i}", cat=pulp.LpBinary) for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f"x_distributed_scan_{i}", cat=pulp.LpBinary) for i in range(N)]

# Objective function
problem += (
    pulp.lpSum([central_cost * data['processing_times']['central']['isolate'][i] * x_central_isolate[i]
                + central_cost * data['processing_times']['central']['scan'][i] * x_central_scan[i]
                + distributed_cost * data['processing_times']['distributed']['isolate'][i] * x_distributed_isolate[i]
                + distributed_cost * data['processing_times']['distributed']['scan'][i] * x_distributed_scan[i]
                for i in range(N)])
)

# Constraints
# Each cluster should have exactly one intervention
for i in range(N):
    problem += (
        x_central_isolate[i] + x_central_scan[i] + x_distributed_isolate[i] + x_distributed_scan[i] == 1
    )

# Maximum central processing time
problem += (
    pulp.lpSum([data['processing_times']['central']['isolate'][i] * x_central_isolate[i]
                + data['processing_times']['central']['scan'][i] * x_central_scan[i]
                for i in range(N)]) <= max_central
)

# Maximum distributed processing time
problem += (
    pulp.lpSum([data['processing_times']['distributed']['isolate'][i] * x_distributed_isolate[i]
                + data['processing_times']['distributed']['scan'][i] * x_distributed_scan[i]
                for i in range(N)]) <= max_distributed
)

# Solve the problem
problem.solve()

# Extracting results
interventions = []
total_cost = pulp.value(problem.objective)

for i in range(N):
    intervention_type = None
    method = None
    amount = 0
    
    if pulp.value(x_central_isolate[i]) == 1:
        intervention_type = 'isolate'
        method = 'central'
        amount = data['processing_times']['central']['isolate'][i]
    elif pulp.value(x_central_scan[i]) == 1:
        intervention_type = 'scan'
        method = 'central'
        amount = data['processing_times']['central']['scan'][i]
    elif pulp.value(x_distributed_isolate[i]) == 1:
        intervention_type = 'isolate'
        method = 'distributed'
        amount = data['processing_times']['distributed']['isolate'][i]
    elif pulp.value(x_distributed_scan[i]) == 1:
        intervention_type = 'scan'
        method = 'distributed'
        amount = data['processing_times']['distributed']['scan'][i]
        
    interventions.append({
        "cluster_id": i+1,
        "type": intervention_type,
        "method": method,
        "amount": amount
    })

# Output the result
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')