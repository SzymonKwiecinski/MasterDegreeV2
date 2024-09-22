import json
import pulp

# Load data from JSON format
data = json.loads("{'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}")

# Extracting data
processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

clusters = range(len(processing_times['central']['isolate']))  # Assuming N clusters

# Create optimization problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention",
    ((cluster, intervention_type, method) 
     for cluster in clusters 
     for intervention_type in ['isolate', 'scan'] 
     for method in ['central', 'distributed']),
    lowBound=0,
    cat='Continuous'
)

# Objective function
problem += pulp.lpSum(intervention_vars[(c, it, 'central')] * (central_cost * processing_times['central'][it][c] for it in ['isolate', 'scan']) +
                      intervention_vars[(c, it, 'distributed')] * (distributed_cost * processing_times['distributed'][it][c] for it in ['isolate', 'scan'])
                      for c in clusters), "Total_Cost"

# Constraints for maximum hours
for method in ['central', 'distributed']:
    for it in ['isolate', 'scan']:
        problem += pulp.lpSum(intervention_vars[(c, it, method)] * processing_times[method][it][c] for c in clusters) <= (max_central if method == 'central' else max_distributed), f"Max_{method.capitalize()}_{it}"

# Solve the problem
problem.solve()

# Prepare output
interventions = []
total_cost = pulp.value(problem.objective)

for c in clusters:
    for it in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            amount = intervention_vars[(c, it, method)].varValue
            if amount > 0:
                interventions.append({
                    "cluster_id": c,
                    "type": it,
                    "method": method,
                    "amount": amount
                })

# Output the solution
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')