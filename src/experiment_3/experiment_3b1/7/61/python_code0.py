import pulp
import json

# Data in JSON format
data = json.loads("""
{
    "processing_times": {
        "central": {
            "isolate": [10, 6, 8],
            "scan": [6, 4, 6]
        },
        "distributed": {
            "isolate": [12, 9, 12],
            "scan": [18, 10, 15]
        }
    },
    "costs": {
        "central": 150,
        "distributed": 70
    },
    "max_hours": {
        "central_max_hours": 16,
        "distributed_max_hours": 33
    }
}
""")

# Parameters
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
c_c = data['costs']['central']
c_d = data['costs']['distributed']
H_c = data['max_hours']['central_max_hours']
H_d = data['max_hours']['distributed_max_hours']

# Problem definition
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
    ((i, j, k) for i in range(N) for j in range(1, 3) for k in range(1, 3)), 
    lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(c_c * (x[(i, 1, 1)] * isolate_central[i] + x[(i, 2, 1)] * scan_central[i]) +
                      c_d * (x[(i, 1, 2)] * isolate_distributed[i] + x[(i, 2, 2)] * scan_distributed[i]) 
                      for i in range(N)), "Total_Cost"

# Constraints
problem += pulp.lpSum(x[(i, 1, 1)] * isolate_central[i] + x[(i, 2, 1)] * scan_central[i] for i in range(N)) <= H_c, "Max_Central_Hours"
problem += pulp.lpSum(x[(i, 1, 2)] * isolate_distributed[i] + x[(i, 2, 2)] * scan_distributed[i] for i in range(N)) <= H_d, "Max_Distributed_Hours"

# Intervention type consistency
for i in range(N):
    for k in range(1, 3):
        problem += x[(i, 1, k)] + x[(i, 2, k)] == 1, f"Intervention_Consistency_{i}_{k}"

# Solve the problem
problem.solve()

# Output the results
for i in range(N):
    for j in range(1, 3):
        for k in range(1, 3):
            if pulp.value(x[(i, j, k)]) > 0:
                print(f'Cluster {i+1}, Intervention Type {j}, Method {k}, Amount: {pulp.value(x[(i, j, k)])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')