import pulp
import json

# Input data in JSON format
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting data from the input
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the LP problem
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), 0, None, pulp.LpInteger)

# Objective Function: Minimize total cost
total_cost = pulp.lpSum([
    interventions[i]['isolate']['central'] * (central_cost * data['processing_times']['central']['isolate'][i] / 60) +
    interventions[i]['isolate']['distributed'] * (distributed_cost * data['processing_times']['distributed']['isolate'][i] / 60) +
    interventions[i]['scan']['central'] * (central_cost * data['processing_times']['central']['scan'][i] / 60) +
    interventions[i]['scan']['distributed'] * (distributed_cost * data['processing_times']['distributed']['scan'][i] / 60)
    for i in range(N)
])
problem += total_cost

# Constraints for maximum hours
problem += pulp.lpSum([interventions[i]['isolate']['central'] * data['processing_times']['central']['isolate'][i] + 
                       interventions[i]['scan']['central'] * data['processing_times']['central']['scan'][i] 
                       for i in range(N)]) <= max_central, "Max_Central_Hours"

problem += pulp.lpSum([interventions[i]['isolate']['distributed'] * data['processing_times']['distributed']['isolate'][i] + 
                       interventions[i]['scan']['distributed'] * data['processing_times']['distributed']['scan'][i] 
                       for i in range(N)]) <= max_distributed, "Max_Distributed_Hours"

# Each cluster must have exactly one type of intervention
for i in range(N):
    problem += pulp.lpSum([interventions[i]['isolate']['central'], interventions[i]['isolate']['distributed'], 
                           interventions[i]['scan']['central'], interventions[i]['scan']['distributed']]) == 1, f"One_Intervention_Cluster_{i}"

# Solve the problem
problem.solve()

# Prepare output
intervention_results = []
for i in range(N):
    for intervention_type in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            amount = interventions[i][intervention_type][method].varValue
            if amount > 0:
                intervention_results.append({
                    "cluster_id": i,
                    "type": intervention_type,
                    "method": method,
                    "amount": amount
                })

total_cost_value = pulp.value(problem.objective)

# Output result
output = {
    "interventions": intervention_results,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')