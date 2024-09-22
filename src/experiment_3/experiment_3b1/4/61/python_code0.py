import pulp
import json

# Data in JSON format
data = json.loads('{"processing_times": {"central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]}, "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}}, "costs": {"central": 150, "distributed": 70}, "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}}')

# Parameters
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
C = ['isolate', 'scan']  # Intervention types
M = ['central', 'distributed']  # Processing methods

# Costs and maximum hours
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem variable
problem = pulp.LpProblem("Intrusion_Intervention_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), C, M), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    (central_cost if k == 'central' else distributed_cost) *
    (data['processing_times'][k][j][i] * x[i][j][k]
     for i in range(N) for j in C for k in M)
), "Total_Cost"

# Constraints

# Each cluster must have exactly one intervention
for i in range(N):
    problem += pulp.lpSum(x[i][j][k] for j in C for k in M) == 1, f"One_intervention_per_cluster_{i}"

# Central processing time constraint
problem += pulp.lpSum(
    data['processing_times']['central']['isolate'][i] * x[i]['isolate']['central'] +
    data['processing_times']['central']['scan'][i] * x[i]['scan']['central']
    for i in range(N)
) <= max_central, "Central_Processing_Time_Constraint"

# Distributed processing time constraint
problem += pulp.lpSum(
    data['processing_times']['distributed']['isolate'][i] * x[i]['isolate']['distributed'] +
    data['processing_times']['distributed']['scan'][i] * x[i]['scan']['distributed']
    for i in range(N)
) <= max_distributed, "Distributed_Processing_Time_Constraint"

# Solve the problem
problem.solve()

# Output the interventions and the total cost
interventions = []
for i in range(N):
    for j in C:
        for k in M:
            if x[i][j][k].varValue == 1:
                interventions.append((i + 1, j, k, data['processing_times'][k][j][i]))

print("Interventions:", interventions)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')