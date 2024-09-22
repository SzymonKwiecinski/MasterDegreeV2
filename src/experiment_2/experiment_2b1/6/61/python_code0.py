import json
import pulp

# Load the data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting relevant parameters
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])  # Number of clusters

# Create a linear programming problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", 
                                       (range(N), ["isolate", "scan"], ["central", "distributed"]), 
                                       cat='Binary')

# Objective function: minimize total cost
total_cost = pulp.lpSum(
    (interventions[i]['isolate']['central'] * costs['central'] * processing_times['central']['isolate'][i] +
     interventions[i]['scan']['central'] * costs['central'] * processing_times['central']['scan'][i] +
     interventions[i]['isolate']['distributed'] * costs['distributed'] * processing_times['distributed']['isolate'][i] +
     interventions[i]['scan']['distributed'] * costs['distributed'] * processing_times['distributed']['scan'][i]) 
    for i in range(N))

problem += total_cost

# Constraints for maximum hours
problem += pulp.lpSum(interventions[i]['isolate']['central'] * processing_times['central']['isolate'][i] +
                      interventions[i]['scan']['central'] * processing_times['central']['scan'][i] 
                      for i in range(N)) <= max_hours['central_max_hours']

problem += pulp.lpSum(interventions[i]['isolate']['distributed'] * processing_times['distributed']['isolate'][i] +
                      interventions[i]['scan']['distributed'] * processing_times['distributed']['scan'][i] 
                      for i in range(N)) <= max_hours['distributed_max_hours']

# Each cluster must have one intervention type
for i in range(N):
    problem += pulp.lpSum(interventions[i]['isolate'][method] for method in ["central", "distributed"]) + \
               pulp.lpSum(interventions[i]['scan'][method] for method in ["central", "distributed"]) == 1

# Solve the problem
problem.solve()

# Prepare the output
intervention_details = []
for i in range(N):
    for method in ["central", "distributed"]:
        for intervention_type in ["isolate", "scan"]:
            if pulp.value(interventions[i][intervention_type][method]) == 1:
                intervention_details.append({
                    "cluster_id": i + 1,
                    "type": intervention_type,
                    "method": method,
                    "amount": processing_times[method][intervention_type][i]
                })

total_cost_value = pulp.value(problem.objective)

# Output the result in the specified format
output = {
    "interventions": intervention_details,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')