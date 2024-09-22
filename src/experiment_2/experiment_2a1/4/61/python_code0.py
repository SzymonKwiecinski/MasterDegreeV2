import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), lowBound=0, cat='Binary')

# Objective function: minimize total cost
problem += pulp.lpSum(
    (central_cost * (data['processing_times']['central'][intervention_type][i] / 60) * interventions[i][intervention_type]['central'] +
     distributed_cost * (data['processing_times']['distributed'][intervention_type][i] / 60) * interventions[i][intervention_type]['distributed'] )
    for i in range(N) for intervention_type in ['isolate', 'scan']
)

# Constraints for max hours on central processing
problem += pulp.lpSum(
    (data['processing_times']['central']['isolate'][i] * interventions[i][ 'isolate']['central'] +
     data['processing_times']['central']['scan'][i] * interventions[i]['scan']['central'])
    for i in range(N)
) <= max_central, "Max_Central_Hours"

# Constraints for max hours on distributed processing
problem += pulp.lpSum(
    (data['processing_times']['distributed']['isolate'][i] * interventions[i]['isolate']['distributed'] +
     data['processing_times']['distributed']['scan'][i] * interventions[i]['scan']['distributed'])
    for i in range(N)
) <= max_distributed, "Max_Distributed_Hours"

# Each cluster must have exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(interventions[i][intervention_type][method] for intervention_type in ['isolate', 'scan'] for method in ['central', 'distributed']) == 1, f"One_Intervention_{i}"

# Solve the problem
problem.solve()

# Output result
result = {"interventions": [], "total_cost": pulp.value(problem.objective)}

for i in range(N):
    for intervention_type in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(interventions[i][intervention_type][method]) == 1:
                result["interventions"].append({
                    "cluster_id": i + 1,
                    "type": intervention_type,
                    "method": method,
                    "amount": data['processing_times'][method][intervention_type][i]
                })

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')