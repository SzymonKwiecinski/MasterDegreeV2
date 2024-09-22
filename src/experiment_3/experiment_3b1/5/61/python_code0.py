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

# Extracting data from JSON
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(central_isolate)  # Assuming the same number of clusters for both processing types

# Create a linear programming problem
problem = pulp.LpProblem("Intrusion_Intervention_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), cat='Binary')

# Objective Function
problem += pulp.lpSum((central_isolate[i] * x[(i, 'isolate', 'central')] + central_scan[i] * x[(i, 'scan', 'central')]) * central_cost +
                       (distributed_isolate[i] * x[(i, 'isolate', 'distributed')] + distributed_scan[i] * x[(i, 'scan', 'distributed')]) * distributed_cost
                       for i in range(N)), "Total_Cost"

# Constraints

# 1. Each cluster must have exactly one intervention type applied
for i in range(N):
    problem += (pulp.lpSum(x[(i, j, k)] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1, f"One_intervention_per_cluster_{i}")

# 2. Maximum processing hours for central processing
problem += (pulp.lpSum((central_isolate[i] * x[(i, 'isolate', 'central')] + central_scan[i] * x[(i, 'scan', 'central')]) for i in range(N)) <= max_central, "Max_Central_Processing_Hours")

# 3. Maximum processing hours for distributed processing
problem += (pulp.lpSum((distributed_isolate[i] * x[(i, 'isolate', 'distributed')] + distributed_scan[i] * x[(i, 'scan', 'distributed')]) for i in range(N)) <= max_distributed, "Max_Distributed_Processing_Hours")

# Solve the problem
problem.solve()

# Output the results
interventions = []

for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(x[(i, j, k)]) == 1:
                interventions.append({
                    "cluster_id": i,
                    "type": j,
                    "method": k,
                    "amount": central_isolate[i] if k == 'central' and j == 'isolate' else
                             central_scan[i] if k == 'central' and j == 'scan' else
                             distributed_isolate[i] if k == 'distributed' and j == 'isolate' else
                             distributed_scan[i]
                })

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')