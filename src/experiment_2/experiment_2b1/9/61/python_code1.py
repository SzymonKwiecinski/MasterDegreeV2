import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting values from data
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Intervention_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']), 
                                        cat='Binary')

# Objective function
problem += (pulp.lpSum(interventions[i]['isolate_central'] * central_cost * data['processing_times']['central']['isolate'][i] / 60 +
                       interventions[i]['scan_central'] * central_cost * data['processing_times']['central']['scan'][i] / 60 +
                       interventions[i]['isolate_distributed'] * distributed_cost * data['processing_times']['distributed']['isolate'][i] / 60 +
                       interventions[i]['scan_distributed'] * distributed_cost * data['processing_times']['distributed']['scan'][i] / 60
                       for i in range(N))), "Total_Cost"

# Constraints for central max hours
problem += (pulp.lpSum(interventions[i]['isolate_central'] * data['processing_times']['central']['isolate'][i] +
                       interventions[i]['scan_central'] * data['processing_times']['central']['scan'][i]
                       for i in range(N)) <= max_central, "Max_Central_Hours")

# Constraints for distributed max hours
problem += (pulp.lpSum(interventions[i]['isolate_distributed'] * data['processing_times']['distributed']['isolate'][i] +
                       interventions[i]['scan_distributed'] * data['processing_times']['distributed']['scan'][i]
                       for i in range(N)) <= max_distributed, "Max_Distributed_Hours")

# Each cluster must be treated with one intervention type
for i in range(N):
    problem += (pulp.lpSum([interventions[i]['isolate_central'], interventions[i]['scan_central'], 
                             interventions[i]['isolate_distributed'], interventions[i]['scan_distributed']]) == 1, 
                  f"One_Intervention_Cluster_{i}")

# Solve the problem
problem.solve()

# Output the interventions and total cost
interventions_output = []
for i in range(N):
    if interventions[i]['isolate_central'].varValue == 1:
        interventions_output.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": data['processing_times']['central']['isolate'][i]})
    elif interventions[i]['scan_central'].varValue == 1:
        interventions_output.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": data['processing_times']['central']['scan'][i]})
    elif interventions[i]['isolate_distributed'].varValue == 1:
        interventions_output.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": data['processing_times']['distributed']['isolate'][i]})
    elif interventions[i]['scan_distributed'].varValue == 1:
        interventions_output.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": data['processing_times']['distributed']['scan'][i]})
        
total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions_output,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')