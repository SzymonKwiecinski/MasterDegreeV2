import pulp
import json

# Data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

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

# Create the Problem
problem = pulp.LpProblem("MILP_Intervention_Selection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Intervention", 
                           ((i, j) for i in range(N) for j in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']), 
                           cat='Binary')

# Objective Function
cost_terms = []
for i in range(N):
    cost_terms.append(
        x[(i, 'isolate_central')] * isolate_central[i] * central_cost +
        x[(i, 'scan_central')] * scan_central[i] * central_cost +
        x[(i, 'isolate_distributed')] * isolate_distributed[i] * distributed_cost +
        x[(i, 'scan_distributed')] * scan_distributed[i] * distributed_cost
    )
problem += pulp.lpSum(cost_terms)

# Constraints
# Each cluster must be assigned exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']) == 1

# Central processing time should not exceed max hours
problem += pulp.lpSum(
    x[(i, 'isolate_central')] * isolate_central[i] +
    x[(i, 'scan_central')] * scan_central[i] for i in range(N)
) <= max_central

# Distributed processing time should not exceed max hours
problem += pulp.lpSum(
    x[(i, 'isolate_distributed')] * isolate_distributed[i] +
    x[(i, 'scan_distributed')] * scan_distributed[i] for i in range(N)
) <= max_distributed

# Solve the problem
problem.solve()

# Output the results
interventions = []
for i in range(N):
    for intervention_type in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']:
        if pulp.value(x[(i, intervention_type)]) == 1:
            method = 'central' if 'central' in intervention_type else 'distributed'
            type_of_intervention = 'isolate' if 'isolate' in intervention_type else 'scan'
            amount = isolate_central[i] if 'isolate' in intervention_type and 'central' in intervention_type else scan_central[i] if 'scan' in intervention_type and 'central' in intervention_type else isolate_distributed[i] if 'isolate' in intervention_type and 'distributed' in intervention_type else scan_distributed[i]
            interventions.append({"cluster_id": i + 1, "type": type_of_intervention, "method": method, "amount": amount})

total_cost = pulp.value(problem.objective)

# Formatting the output
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')