import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

N = len(data['processing_times']['central']['isolate'])  # Number of clusters
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

# Create the optimization problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), 
                                        lowBound=0, cat='Binary')

# Objective function: Total cost
problem += pulp.lpSum(
    interventions[i][j][k] * processing_times['central'][j][i] * costs['central'] + 
    interventions[i][j][k] * processing_times['distributed'][j][i] * costs['distributed'] 
    for i in range(N) 
    for j in ['isolate', 'scan'] 
    for k in ['central', 'distributed']
), "Total_Cost"

# Constraints for maximum hours
for k in ['central', 'distributed']:
    problem += pulp.lpSum(
        interventions[i][j][k] * processing_times[k][j][i] for i in range(N) for j in ['isolate', 'scan']
    ) <= max_hours[f"{k}_max_hours"], f"Max_{k.capitalize()}_Hours"

# Constraint to ensure one intervention type per cluster
for i in range(N):
    problem += pulp.lpSum(interventions[i][j][k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1, f"One_Intervention_Cluster_{i+1}"

# Solve the problem
problem.solve()

# Prepare output
interventions_result = []
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(interventions[i][j][k]) == 1:
                interventions_result.append({
                    "cluster_id": i + 1,
                    "type": j,
                    "method": k,
                    "amount": processing_times[k][j][i]
                })

total_cost = pulp.value(problem.objective)

# Output
output = {
    "interventions": interventions_result,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))

# Print objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')