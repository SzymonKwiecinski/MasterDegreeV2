import pulp
import json

data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Parse the input data
processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(processing_times['central']['isolate'])  # Number of clusters

# Create the LP problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
interventions = pulp.LpVariable.dicts("Intervention", ((i, intervention_type, method) 
                      for i in range(N) 
                      for intervention_type in ['isolate', 'scan'] 
                      for method in ['central', 'distributed']), 
                      lowBound=0, cat='Binary')

# Objective Function
total_cost = pulp.lpSum(
    interventions[i, 'isolate', 'central'] * (processing_times['central']['isolate'][i] * central_cost) +
    interventions[i, 'scan', 'central'] * (processing_times['central']['scan'][i] * central_cost) +
    interventions[i, 'isolate', 'distributed'] * (processing_times['distributed']['isolate'][i] * distributed_cost) +
    interventions[i, 'scan', 'distributed'] * (processing_times['distributed']['scan'][i] * distributed_cost)
    for i in range(N)
)
problem += total_cost

# Constraints for maximum hours
for method in ['central', 'distributed']:
    problem += pulp.lpSum(
        interventions[i, 'isolate', method] * processing_times[method]['isolate'][i] +
        interventions[i, 'scan', method] * processing_times[method]['scan'][i]
        for i in range(N)
    ) <= (max_central if method == 'central' else max_distributed)

# Ensure each cluster gets exactly one intervention method
for i in range(N):
    problem += pulp.lpSum(interventions[i, intervention_type, method] for intervention_type in ['isolate', 'scan'] for method in ['central', 'distributed']) == 1

# Solve the problem
problem.solve()

# Prepare output 
interventions_output = []
for i in range(N):
    for intervention_type in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(interventions[i, intervention_type, method]) == 1:
                interventions_output.append({
                    "cluster_id": i,
                    "type": intervention_type,
                    "method": method,
                    "amount": 1
                })

total_cost_value = pulp.value(problem.objective)

output = {
    "interventions": interventions_output,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')