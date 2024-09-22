import pulp
import json

# Load data from the provided JSON format
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Define problem parameters
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the optimization problem
problem = pulp.LpProblem("Intervention_Cost_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", 
                                       [(i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']],
                                       lowBound=0, 
                                       cat='Binary')

# Objective function
problem += pulp.lpSum(interventions[(i, 'isolate', 'central')] * (data['processing_times']['central']['isolate'][i] * central_cost) +
                       interventions[(i, 'scan', 'central')] * (data['processing_times']['central']['scan'][i] * central_cost) +
                       interventions[(i, 'isolate', 'distributed')] * (data['processing_times']['distributed']['isolate'][i] * distributed_cost) +
                       interventions[(i, 'scan', 'distributed')] * (data['processing_times']['distributed']['scan'][i] * distributed_cost)
                       for i in range(N))

# Constraints for maximum hours
for method in ['central', 'distributed']:
    max_hours = max_central if method == 'central' else max_distributed
    problem += pulp.lpSum(interventions[(i, 'isolate', method)] * data['processing_times'][method]['isolate'][i] +
                           interventions[(i, 'scan', method)] * data['processing_times'][method]['scan'][i]
                           for i in range(N)) <= max_hours

# Constraints for treatment consistency per cluster
for i in range(N):
    problem += pulp.lpSum(interventions[(i, 'isolate', 'central')] + interventions[(i, 'scan', 'central')] +
                           interventions[(i, 'isolate', 'distributed')] + interventions[(i, 'scan', 'distributed')]) == 1

# Solve the problem
problem.solve()

# Prepare output
interventions_output = []
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(interventions[(i, j, k)]) == 1:
                interventions_output.append({
                    "cluster_id": i,
                    "type": j,
                    "method": k,
                    "amount": pulp.value(interventions[(i, j, k)])
                })

total_cost = pulp.value(problem.objective)

# Output format
output = {
    "interventions": interventions_output,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')