import pulp
import json

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
                             'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 
        'costs': {'central': 150, 'distributed': 70}, 
        'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extracting data from the input
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])  # Number of clusters

# Create the problem
problem = pulp.LpProblem("Intervention_Cost_Optimization", pulp.LpMinimize)

# Decision variables
interventions = pulp.LpVariable.dicts("Intervention", (range(N), ['isolate', 'scan'], ['central', 'distributed']), 
                                       lowBound=0, cat='Binary')

# Objective function: minimize total cost
total_cost = pulp.lpSum([interventions[i][t][m] * 
                          (costs[m] * (processing_times[m][t][i] / 60)) for i in range(N) for t in ['isolate', 'scan'] for m in ['central', 'distributed']])
problem += total_cost

# Constraints for maximum hours
problem += pulp.lpSum([interventions[i]['isolate']['central'] * processing_times['central']['isolate'][i] + 
                        interventions[i]['scan']['central'] * processing_times['central']['scan'][i] for i in range(N)]) <= max_hours['central_max_hours'], "Central_Max_Hours"

problem += pulp.lpSum([interventions[i]['isolate']['distributed'] * processing_times['distributed']['isolate'][i] + 
                        interventions[i]['scan']['distributed'] * processing_times['distributed']['scan'][i] for i in range(N)]) <= max_hours['distributed_max_hours'], "Distributed_Max_Hours"

# Each cluster must be treated with one intervention type consistently
for i in range(N):
    problem += pulp.lpSum([interventions[i][t][m] for t in ['isolate', 'scan'] for m in ['central', 'distributed']]) == 1, f"Single_Intervention_{i}"

# Solve the problem
problem.solve()

# Prepare output
output = {"interventions": [], "total_cost": pulp.value(problem.objective)}

for i in range(N):
    for t in ['isolate', 'scan']:
        for m in ['central', 'distributed']:
            if pulp.value(interventions[i][t][m]) == 1:
                output["interventions"].append({"cluster_id": i + 1, "type": t, "method": m, "amount": 1})

# Print the output as specified
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')