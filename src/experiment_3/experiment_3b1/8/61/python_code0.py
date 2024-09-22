import pulp
import json

# Data Input
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

# Problem Definition
problem = pulp.LpProblem("Intervention_Strategy", pulp.LpMinimize)

# Variables
clusters = range(len(data['processing_times']['central']['isolate']))
interventions = ['isolate', 'scan']
methods = ['central', 'distributed']

x = pulp.LpVariable.dicts("x", 
                           ((i, j, k) for i in clusters for j in interventions for k in methods), 
                           cat='Binary')

# Cost Calculation
cost = {}
for i in clusters:
    for j in interventions:
        for k in methods:
            if k == 'central':
                cost[i, j, k] = data['costs']['central'] * (data['processing_times']['central'][j][i] / 1)
            else:
                cost[i, j, k] = data['costs']['distributed'] * (data['processing_times']['distributed'][j][i] / 1)

# Objective Function
problem += pulp.lpSum(cost[i, j, k] * x[i, j, k] for i in clusters for j in interventions for k in methods)

# Constraints

# Single Intervention Type per Cluster
for i in clusters:
    problem += pulp.lpSum(x[i, j, k] for j in interventions for k in methods) == 1

# Central Processing Time Constraint
problem += pulp.lpSum(data['processing_times']['central'][j][i] * x[i, j, 'central'] for i in clusters for j in interventions) <= data['max_hours']['central_max_hours']

# Distributed Processing Time Constraint
problem += pulp.lpSum(data['processing_times']['distributed'][j][i] * x[i, j, 'distributed'] for i in clusters for j in interventions) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Output the results
results = []
for i in clusters:
    for j in interventions:
        for k in methods:
            if pulp.value(x[i, j, k]) == 1:
                results.append({
                    'cluster_id': i + 1,  # +1 for cluster ID starting from 1
                    'type': j,
                    'method': k,
                    'amount': 1
                })

total_cost = pulp.value(problem.objective)

# Printing the objective
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
# Print the interventions
print({"interventions": results, "total_cost": total_cost})