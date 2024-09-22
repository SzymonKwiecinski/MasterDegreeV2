import json
import pulp

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Parsing input data
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])

# Create problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), cat='Binary')

# Objective function
problem += pulp.lpSum(
    intervention_vars[i][intervention][method] * 
    (processing_times[method][intervention][i] * costs[method])
    for i in range(N) for intervention in ['isolate', 'scan'] for method in ['central', 'distributed']
)

# Constraints for max hours
for method in ['central', 'distributed']:
    problem += pulp.lpSum(
        intervention_vars[i][intervention][method] * processing_times[method][intervention][i]
        for i in range(N) for intervention in ['isolate', 'scan']
    ) <= max_hours[f"{method}_max_hours"]

# Ensuring each cluster is treated consistently
for i in range(N):
    problem += pulp.lpSum(
        intervention_vars[i][intervention][method] 
        for intervention in ['isolate', 'scan'] for method in ['central', 'distributed']
    ) == 1

# Solve the problem
problem.solve()

# Prepare output
interventions = []
for i in range(N):
    for intervention in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if intervention_vars[i][intervention][method].value() == 1:
                interventions.append({
                    "cluster_id": i + 1,
                    "type": intervention,
                    "method": method,
                    "amount": processing_times[method][intervention][i]
                })

# Total cost
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

# Printing results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')