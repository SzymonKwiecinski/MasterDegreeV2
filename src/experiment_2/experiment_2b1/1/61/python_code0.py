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

# Problem definition
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision Variables
interventions = pulp.LpVariable.dicts("Intervention", 
    [(i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']], 
    cat='Binary')

# Objective Function
total_cost = pulp.lpSum([
    interventions[i, 'isolate', 'central'] * central_cost * data['processing_times']['central']['isolate'][i] +
    interventions[i, 'scan', 'central'] * central_cost * data['processing_times']['central']['scan'][i] +
    interventions[i, 'isolate', 'distributed'] * distributed_cost * data['processing_times']['distributed']['isolate'][i] +
    interventions[i, 'scan', 'distributed'] * distributed_cost * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
])
problem += total_cost

# Constraints
for i in range(N):
    # Each cluster must have exactly one intervention
    problem += pulp.lpSum(interventions[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# Max hours constraints
problem += pulp.lpSum(interventions[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] +
                      interventions[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i] 
                      for i in range(N)) <= max_central

problem += pulp.lpSum(interventions[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] +
                      interventions[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i] 
                      for i in range(N)) <= max_distributed

# Solve the problem
problem.solve()

# Collecting output
interventions_output = []
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(interventions[i, j, k]) == 1:
                interventions_output.append({
                    "cluster_id": i + 1,
                    "type": j,
                    "method": k,
                    "amount": data['processing_times'][k][j][i]
                })

total_cost_value = pulp.value(problem.objective)

# Print the results
output = {
    "interventions": interventions_output,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')