import json
import pulp

data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Parse input data
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

clusters = range(len(processing_times['central']['isolate']))

# Create the LP problem
problem = pulp.LpProblem('Intervention_Optimization', pulp.LpMinimize)

# Create decision variables
interventions = pulp.LpVariable.dicts("intervention", (clusters, ['isolate', 'scan'], ['central', 'distributed']), lowBound=0)

# Objective function: minimize total cost
problem += pulp.lpSum(
    interventions[i][t][m] * (
        (costs['central'] * processing_times['central'][t][i]) if m == 'central' else (costs['distributed'] * processing_times['distributed'][t][i])
    )
    for i in clusters for t in ['isolate', 'scan'] for m in ['central', 'distributed']
)

# Constraints for max hours
problem += pulp.lpSum(
    interventions[i]['isolate']['central'] * processing_times['central']['isolate'][i] for i in clusters
) <= max_hours['central_max_hours']

problem += pulp.lpSum(
    interventions[i]['scan']['central'] * processing_times['central']['scan'][i] for i in clusters
) <= max_hours['central_max_hours']

problem += pulp.lpSum(
    interventions[i]['isolate']['distributed'] * processing_times['distributed']['isolate'][i] for i in clusters
) <= max_hours['distributed_max_hours']

problem += pulp.lpSum(
    interventions[i]['scan']['distributed'] * processing_times['distributed']['scan'][i] for i in clusters
) <= max_hours['distributed_max_hours']

# Each cluster must have one intervention type consistently
for i in clusters:
    problem += pulp.lpSum([interventions[i]['isolate']['central'], interventions[i]['isolate']['distributed'], interventions[i]['scan']['central'], interventions[i]['scan']['distributed']]) == 1

# Solve the problem
problem.solve()

# Prepare output
output = {
    "interventions": [
        {
            "cluster_id": i,
            "type": t,
            "method": m,
            "amount": pulp.value(interventions[i][t][m])
        }
        for i in clusters for t in ['isolate', 'scan'] for m in ['central', 'distributed'] if pulp.value(interventions[i][t][m]) > 0
    ],
    "total_cost": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')