import json
import pulp

data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting data from JSON
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])  # Number of clusters

# Create the LP problem
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention", [(i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']], lowBound=0, cat='Binary')

# Objective function: total cost
total_cost = pulp.lpSum([
    intervention_vars[(i, 'isolate', 'central')] * processing_times['central']['isolate'][i] * costs['central'] / 60 +
    intervention_vars[(i, 'scan', 'central')] * processing_times['central']['scan'][i] * costs['central'] / 60 +
    intervention_vars[(i, 'isolate', 'distributed')] * processing_times['distributed']['isolate'][i] * costs['distributed'] / 60 +
    intervention_vars[(i, 'scan', 'distributed')] * processing_times['distributed']['scan'][i] * costs['distributed'] / 60
    for i in range(N)
])
problem += total_cost, "Total_Cost"

# Constraints for maximum hours
for j in ['central', 'distributed']:
    problem += pulp.lpSum([
        intervention_vars[(i, 'isolate', j)] * processing_times[j]['isolate'][i] +
        intervention_vars[(i, 'scan', j)] * processing_times[j]['scan'][i]
        for i in range(N)
    ]) <= max_hours[f"{j}_max_hours"], f"Max_Hours_{j}"

# Each cluster must have exactly one intervention type and method
for i in range(N):
    problem += pulp.lpSum([
        intervention_vars[(i, 'isolate', 'central')],
        intervention_vars[(i, 'scan', 'central')],
        intervention_vars[(i, 'isolate', 'distributed')],
        intervention_vars[(i, 'scan', 'distributed')]
    ]) == 1, f"One_Intervention_Per_Cluster_{i}"

# Solve the problem
problem.solve()

# Output the results
interventions_output = []
total_cost_value = pulp.value(problem.objective)

for i in range(N):
    for intervention in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(intervention_vars[(i, intervention, method)]) == 1:
                interventions_output.append({
                    "cluster_id": i,
                    "type": intervention,
                    "method": method,
                    "amount": pulp.value(intervention_vars[(i, intervention, method)])
                })

output = {
    "interventions": interventions_output,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')