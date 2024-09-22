import pulp
import json

# Load the data from the provided JSON format
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extract data
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])

# Create the LP problem
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), lowBound=0, cat='Binary')

# Objective function: Minimize total cost
total_cost = pulp.lpSum([
    costs['central'] * (processing_times['central']['isolate'][i] * interventions[i]['isolate']['central'] + processing_times['central']['scan'][i] * interventions[i]['scan']['central']) +
    costs['distributed'] * (processing_times['distributed']['isolate'][i] * interventions[i]['isolate']['distributed'] + processing_times['distributed']['scan'][i] * interventions[i]['scan']['distributed'])
    for i in range(N)
])
problem += total_cost

# Constraints for central max hours
problem += pulp.lpSum([
    processing_times['central']['isolate'][i] * interventions[i]['isolate']['central'] + 
    processing_times['central']['scan'][i] * interventions[i]['scan']['central'] 
    for i in range(N)
]) <= max_hours['central_max_hours']

# Constraints for distributed max hours
problem += pulp.lpSum([
    processing_times['distributed']['isolate'][i] * interventions[i]['isolate']['distributed'] + 
    processing_times['distributed']['scan'][i] * interventions[i]['scan']['distributed'] 
    for i in range(N)
]) <= max_hours['distributed_max_hours']

# Each cluster must have one type of intervention
for i in range(N):
    problem += pulp.lpSum([interventions[i]['isolate']['central'], interventions[i]['isolate']['distributed'], interventions[i]['scan']['central'], interventions[i]['scan']['distributed']]) == 1

# Solve the problem
problem.solve()

# Prepare output
output = {'interventions': []}
for i in range(N):
    for intervention_type in ['isolate', 'scan']:
        for method in ['central', 'distributed']:
            if pulp.value(interventions[i][intervention_type][method]) == 1:
                output['interventions'].append({
                    "cluster_id": i + 1,
                    "type": intervention_type,
                    "method": method,
                    "amount": 1
                })

output['total_cost'] = pulp.value(problem.objective)

# Printing the objective value
print(f' (Objective Value): <OBJ>{output["total_cost"]}</OBJ>')