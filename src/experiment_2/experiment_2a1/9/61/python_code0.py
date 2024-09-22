import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Initialize the problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

N = len(data['processing_times']['central']['isolate'])
clusters = range(N)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention",
                                            [(i, j, k) for i in clusters for j in ['isolate', 'scan'] for k in ['central', 'distributed']],
                                            lowBound=0,
                                            upBound=1,
                                            cat='Binary')

# Objective function: total cost
total_cost = pulp.lpSum((data['costs']['central'] * (data['processing_times']['central'][j][i] * intervention_vars[(i, j, 'central')])
                          + data['costs']['distributed'] * (data['processing_times']['distributed'][j][i] * intervention_vars[(i, j, 'distributed')]))
                          for i in clusters for j in ['isolate', 'scan'])

problem += total_cost

# Constraints for maximum hours
problem += pulp.lpSum((data['processing_times']['central']['isolate'][i] * intervention_vars[(i, 'isolate', 'central')] +
                       data['processing_times']['central']['scan'][i] * intervention_vars[(i, 'scan', 'central')]) for i in clusters) <= data['max_hours']['central_max_hours'], "Central_Hours_Max"
                       
problem += pulp.lpSum((data['processing_times']['distributed']['isolate'][i] * intervention_vars[(i, 'isolate', 'distributed')] +
                       data['processing_times']['distributed']['scan'][i] * intervention_vars[(i, 'scan', 'distributed')]) for i in clusters) <= data['max_hours']['distributed_max_hours'], "Distributed_Hours_Max"

# Each cluster must have one intervention type
for i in clusters:
    problem += pulp.lpSum(intervention_vars[(i, 'isolate', 'central')] + intervention_vars[(i, 'scan', 'central')] + 
                            intervention_vars[(i, 'isolate', 'distributed')] + intervention_vars[(i, 'scan', 'distributed')]) == 1, f"One_Intervention_Cluster_{i}"

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in clusters:
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(intervention_vars[(i, j, k)]) == 1:
                interventions.append({
                    "cluster_id": i,
                    "type": j,
                    "method": k,
                    "amount": 1
                })

total_cost_value = pulp.value(problem.objective)

# Output the result
output = {
    "interventions": interventions,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')