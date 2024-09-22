import json
import pulp

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extract data from the input
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])

# Create the optimization problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
interventions = {}
for i in range(N):
    interventions[i] = pulp.LpVariable.dicts("intervention", 
                                               ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed'], 
                                               cat='Binary')

# Objective Function
total_cost = pulp.lpSum([costs['central'] * (processing_times['central']['isolate'][i] * interventions[i]['isolate_central'] + 
                                              processing_times['central']['scan'][i] * interventions[i]['scan_central']) +
                          costs['distributed'] * (processing_times['distributed']['isolate'][i] * interventions[i]['isolate_distributed'] + 
                                                  processing_times['distributed']['scan'][i] * interventions[i]['scan_distributed']) 
                          for i in range(N)])
problem += total_cost

# Constraints
# Central hours constraint
problem += pulp.lpSum([processing_times['central']['isolate'][i] * interventions[i]['isolate_central'] +
                       processing_times['central']['scan'][i] * interventions[i]['scan_central'] for i in range(N)]) <= max_hours['central_max_hours']

# Distributed hours constraint
problem += pulp.lpSum([processing_times['distributed']['isolate'][i] * interventions[i]['isolate_distributed'] +
                       processing_times['distributed']['scan'][i] * interventions[i]['scan_distributed'] for i in range(N)]) <= max_hours['distributed_max_hours']

# Each cluster can have only one intervention type
for i in range(N):
    problem += interventions[i]['isolate_central'] + interventions[i]['scan_central'] + \
               interventions[i]['isolate_distributed'] + interventions[i]['scan_distributed'] == 1

# Solve the problem
problem.solve()

# Prepare output
output = {'interventions': []}
for i in range(N):
    for intervention_type in ['isolate_central', 'scan_central', 'isolate_distributed', 'scan_distributed']:
        if pulp.value(interventions[i][intervention_type]) == 1:
            type = intervention_type.split('_')[0]
            method = intervention_type.split('_')[1]
            output['interventions'].append({
                'cluster_id': i + 1,
                'type': type,
                'method': method,
                'amount': 1  # Since it's a binary variable, amount is either 0 or 1
            })

output['total_cost'] = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{output["total_cost"]}</OBJ>')