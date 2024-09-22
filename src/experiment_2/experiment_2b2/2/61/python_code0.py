import pulp

# Load the data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Number of clusters
N = len(processing_times['central']['isolate'])

# Problem
problem = pulp.LpProblem("Intrusion_Intervention_Problem", pulp.LpMinimize)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention",
                                          [(i, t, m) for i in range(N) 
                                           for t in ['isolate', 'scan'] 
                                           for m in ['central', 'distributed']],
                                          cat='Binary')

# Constraints for each cluster to have one intervention type and one method
for i in range(N):
    problem += pulp.lpSum([intervention_vars[i, t, m] for t in ['isolate', 'scan'] for m in ['central', 'distributed']]) == 1

# Central processing time constraint
problem += pulp.lpSum([intervention_vars[i, 'isolate', 'central'] * processing_times['central']['isolate'][i] +
                       intervention_vars[i, 'scan', 'central'] * processing_times['central']['scan'][i]
                       for i in range(N)]) <= max_central

# Distributed processing time constraint
problem += pulp.lpSum([intervention_vars[i, 'isolate', 'distributed'] * processing_times['distributed']['isolate'][i] +
                       intervention_vars[i, 'scan', 'distributed'] * processing_times['distributed']['scan'][i]
                       for i in range(N)]) <= max_distributed

# Objective function
problem += pulp.lpSum([intervention_vars[i, 'isolate', 'central'] * processing_times['central']['isolate'][i] * central_cost +
                       intervention_vars[i, 'scan', 'central'] * processing_times['central']['scan'][i] * central_cost +
                       intervention_vars[i, 'isolate', 'distributed'] * processing_times['distributed']['isolate'][i] * distributed_cost +
                       intervention_vars[i, 'scan', 'distributed'] * processing_times['distributed']['scan'][i] * distributed_cost
                       for i in range(N)])

# Solve
problem.solve()

# Output
interventions = []
total_cost = pulp.value(problem.objective)
for i in range(N):
    for t in ['isolate', 'scan']:
        for m in ['central', 'distributed']:
            if pulp.value(intervention_vars[i, t, m]) == 1:
                interventions.append({
                    "cluster_id": i + 1,
                    "type": t,
                    "method": m,
                    "amount": 1  # always 1 since it's a Binary decision
                })

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')