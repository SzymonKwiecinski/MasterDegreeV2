import pulp
import json

# Load the data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {
        'central': 150,
        'distributed': 70
    },
    'max_hours': {
        'central_max_hours': 16,
        'distributed_max_hours': 33
    }
}

# Define sets and parameters
N = len(data['processing_times']['central']['isolate'])
C = range(1, N + 1)
T = ['isolate', 'scan']
M = ['central', 'distributed']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, t, m) for i in C for t in T for m in M), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    (data['costs']['central'] * data['processing_times']['central'][t][i-1] * x[(i, t, 'central')] +
     data['costs']['distributed'] * data['processing_times']['distributed'][t][i-1] * x[(i, t, 'distributed')])
    for i in C for t in T
), "Total_Cost"

# Constraints
# Each cluster must have one intervention type consistently applied
for i in C:
    problem += pulp.lpSum(x[(i, t, m)] for t in T for m in M) == 1, f"One_Intervention_Per_Cluster_{i}"

# Central processing time constraint
problem += pulp.lpSum(
    data['processing_times']['central'][t][i-1] * x[(i, t, 'central')] for i in C for t in T
) <= data['max_hours']['central_max_hours'], "Central_Processing_Time"

# Distributed processing time constraint
problem += pulp.lpSum(
    data['processing_times']['distributed'][t][i-1] * x[(i, t, 'distributed')] for i in C for t in T
) <= data['max_hours']['distributed_max_hours'], "Distributed_Processing_Time"

# Solve the problem
problem.solve()

# Print the results
interventions = []
for i in C:
    for t in T:
        for m in M:
            if pulp.value(x[(i, t, m)]) == 1:
                interventions.append({'cluster_id': i, 'type': t, 'method': m})

total_cost = pulp.value(problem.objective)

print(f'Interventions: {interventions}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')