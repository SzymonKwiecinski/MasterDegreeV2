import pulp
import json

# Data provided in JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    }, 
    'costs': {'central': 150, 'distributed': 70}, 
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting data from the JSON format
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
methods = ['central', 'distributed']
interventions = ['isolate', 'scan']

# Create the LP problem
problem = pulp.LpProblem("IntrusionResponseOptimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", 
                           ((i, m, intervention) for i in range(N) for m in methods for intervention in interventions), 
                           cat='Binary')

# Objective Function
problem += pulp.lpSum(data['costs'][m] * 
                       (data['processing_times'][m]['isolate'][i] * x[(i, m, 'isolate')] + 
                        data['processing_times'][m]['scan'][i] * x[(i, m, 'scan')]) 
                       for i in range(N) for m in methods), "Total Cost"

# Constraints
for i in range(N):
    # Each cluster must have one intervention
    problem += pulp.lpSum(x[(i, m, 'isolate')] + x[(i, m, 'scan')] for m in methods) == 1, f"Cluster_{i}_Intervention"

for m in methods:
    # Hours constraint for each method
    problem += pulp.lpSum(data['processing_times'][m]['isolate'][i] * x[(i, m, 'isolate')] + 
                          data['processing_times'][m]['scan'][i] * x[(i, m, 'scan')] for i in range(N)) <= data['max_hours'][f"{m}_max_hours"], f"MaxHours_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')