import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting data
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("intervention", 
                                        ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), 
                                        cat='Binary')

# Objective function
problem += pulp.lpSum(interventions[i, j, k] * (data['processing_times'][k][j][i] * (central_cost if k == 'central' else distributed_cost))
                      for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed'])

# Constraints for processing times
for k in ['central', 'distributed']:
    problem += pulp.lpSum(interventions[i, j, k] * data['processing_times'][k][j][i] for i in range(N) for j in ['isolate', 'scan']) <= (max_central if k == 'central' else max_distributed)

# Each cluster should have exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(interventions[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# Solve the problem
problem.solve()

# Output results
intervention_details = []
total_cost = pulp.value(problem.objective)

for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(interventions[i, j, k]) == 1:
                intervention_details.append({
                    "cluster_id": i + 1,
                    "type": j,
                    "method": k,
                    "amount": data['processing_times'][k][j][i]
                })

output = {
    "interventions": intervention_details,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')