import pulp
import json

# Load data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Define problem
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", 
                                       ((i, type_, method) for i in range(N) for type_ in ['isolate', 'scan'] for method in ['central', 'distributed']), 
                                       lowBound=0, 
                                       cat='Integer')

# Objective function
total_cost = pulp.lpSum(interventions[i, type_, method] * 
                        (data['costs'][method] * 
                         (data['processing_times'][method][type_][i] / 60)) 
                        for i in range(N) for type_ in ['isolate', 'scan'] for method in ['central', 'distributed'])

problem += total_cost

# Constraints for maximum hours for each processing method
problem += pulp.lpSum(interventions[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] for i in range(N)) <= data['max_hours']['central_max_hours']
problem += pulp.lpSum(interventions[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i] for i in range(N)) <= data['max_hours']['central_max_hours']
problem += pulp.lpSum(interventions[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] for i in range(N)) <= data['max_hours']['distributed_max_hours']
problem += pulp.lpSum(interventions[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i] for i in range(N)) <= data['max_hours']['distributed_max_hours']

# Consistency constraints: each cluster must use one intervention type consistently
for i in range(N):
    problem += (pulp.lpSum(interventions[i, 'isolate', method] for method in ['central', 'distributed']) +
                pulp.lpSum(interventions[i, 'scan', method] for method in ['central', 'distributed']) == 1)

# Solve the problem
problem.solve()

# Prepare output
interventions_output = []
for i in range(N):
    for type_ in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            amount = pulp.value(interventions[i, type_, method])
            if amount > 0:
                interventions_output.append({
                    "cluster_id": i + 1,
                    "type": type_,
                    "method": method,
                    "amount": amount
                })

total_cost_value = pulp.value(problem.objective)

# Output the result
output = {
    "interventions": interventions_output,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')