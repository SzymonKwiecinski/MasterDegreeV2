import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting the input data
processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']
N = len(processing_times['central']['isolate'])

# Create the linear programming problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
intervention_vars = pulp.LpVariable.dicts("Intervention", 
                                            [(i, 'isolate', 'central') for i in range(N)] + 
                                            [(i, 'scan', 'central') for i in range(N)] + 
                                            [(i, 'isolate', 'distributed') for i in range(N)] + 
                                            [(i, 'scan', 'distributed') for i in range(N)], 
                                            lowBound=0, 
                                            cat='Binary')

# Objective function
total_cost = pulp.lpSum([intervention_vars[(i, 'isolate', 'central')] * (processing_times['central']['isolate'][i] * central_cost) +
                          intervention_vars[(i, 'scan', 'central')] * (processing_times['central']['scan'][i] * central_cost) +
                          intervention_vars[(i, 'isolate', 'distributed')] * (processing_times['distributed']['isolate'][i] * distributed_cost) +
                          intervention_vars[(i, 'scan', 'distributed')] * (processing_times['distributed']['scan'][i] * distributed_cost) 
                          for i in range(N)])

problem += total_cost, "Total_Cost"

# Constraints for maximum hours
for i in range(N):
    problem += (pulp.lpSum([intervention_vars[(i, 'isolate', 'central')] * processing_times['central']['isolate'][i] + 
                             intervention_vars[(i, 'scan', 'central')] * processing_times['central']['scan'][i]]) <= max_central, 
                       f"Max_Central_Hours_Cluster_{i+1}")

    problem += (pulp.lpSum([intervention_vars[(i, 'isolate', 'distributed')] * processing_times['distributed']['isolate'][i] + 
                             intervention_vars[(i, 'scan', 'distributed')] * processing_times['distributed']['scan'][i]]) <= max_distributed, 
                       f"Max_Distributed_Hours_Cluster_{i+1}")

# Ensure each cluster has exactly one intervention type
for i in range(N):
    problem += (pulp.lpSum([intervention_vars[(i, 'isolate', 'central')], 
                             intervention_vars[(i, 'scan', 'central')], 
                             intervention_vars[(i, 'isolate', 'distributed')], 
                             intervention_vars[(i, 'scan', 'distributed')]]) == 1, 
                 f"One_Intervention_Cluster_{i+1}")

# Solve the problem
problem.solve()

# Preparing output
interventions = []
total_cost_value = pulp.value(problem.objective)

for i in range(N):
    for method in ['central', 'distributed']:
        for intervention_type in ['isolate', 'scan']:
            if pulp.value(intervention_vars[(i, intervention_type, method)]) == 1:
                interventions.append({"cluster_id": i + 1, 
                                      "type": intervention_type, 
                                      "method": method})

# Output
output = {"interventions": interventions, "total_cost": total_cost_value}
print(json.dumps(output, indent=4))

# Print objective value
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')