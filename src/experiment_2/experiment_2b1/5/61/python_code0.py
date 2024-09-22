import pulp
import json

# Data input
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extract data
central_processing_times = data['processing_times']['central']
distributed_processing_times = data['processing_times']['distributed']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']
N = len(central_processing_times['isolate'])  # Assume the number of clusters is the same for each type

# Create the problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']),
                           cat='Binary')

# Objective function
problem += pulp.lpSum([
    (central_cost * central_processing_times['isolate'][i] * x[i]['isolate_central'] +
     central_cost * central_processing_times['scan'][i] * x[i]['scan_central'] +
     distributed_cost * distributed_processing_times['isolate'][i] * x[i]['isolate_distributed'] +
     distributed_cost * distributed_processing_times['scan'][i] * x[i]['scan_distributed'])
    for i in range(N)
]), "Total_Cost"

# Constraints for central processing hours
problem += pulp.lpSum([
    central_processing_times['isolate'][i] * x[i]['isolate_central'] +
    central_processing_times['scan'][i] * x[i]['scan_central']
    for i in range(N)
]) <= max_central, "Central_Hours_Limit"

# Constraints for distributed processing hours
problem += pulp.lpSum([
    distributed_processing_times['isolate'][i] * x[i]['isolate_distributed'] +
    distributed_processing_times['scan'][i] * x[i]['scan_distributed']
    for i in range(N)
]) <= max_distributed, "Distributed_Hours_Limit"

# Each cluster must have exactly one intervention type
for i in range(N):
    problem += (x[i]['isolate_central'] + x[i]['scan_central'] +
                x[i]['isolate_distributed'] + x[i]['scan_distributed'] == 1), f"One_Intervention_Cluster_{i}"

# Solve the problem
problem.solve()

# Prepare output
interventions = []
for i in range(N):
    if pulp.value(x[i]['isolate_central']) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "central", "amount": central_processing_times['isolate'][i]})
    elif pulp.value(x[i]['scan_central']) == 1:
        interventions.append({"cluster_id": i, "type": "scan", "method": "central", "amount": central_processing_times['scan'][i]})
    elif pulp.value(x[i]['isolate_distributed']) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "distributed", "amount": distributed_processing_times['isolate'][i]})
    else:
        interventions.append({"cluster_id": i, "type": "scan", "method": "distributed", "amount": distributed_processing_times['scan'][i]})

total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')