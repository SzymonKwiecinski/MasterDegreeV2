import pulp
import json

# Data input
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting data from the input
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Network_Cluster_Intrusion_Mitigation", pulp.LpMinimize)

# Decision Variables
x_c_I = pulp.LpVariable.dicts("x_c_I", range(N), 0, 1, pulp.LpBinary)
x_d_I = pulp.LpVariable.dicts("x_d_I", range(N), 0, 1, pulp.LpBinary)
x_c_S = pulp.LpVariable.dicts("x_c_S", range(N), 0, 1, pulp.LpBinary)
x_d_S = pulp.LpVariable.dicts("x_d_S", range(N), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum([
    (central_cost * (x_c_I[i] * isolate_central[i] + x_c_S[i] * scan_central[i]) +
     distributed_cost * (x_d_I[i] * isolate_distributed[i] + x_d_S[i] * scan_distributed[i]))
    for i in range(N)
])

# Constraints
for i in range(N):
    problem += x_c_I[i] + x_d_I[i] + x_c_S[i] + x_d_S[i] == 1

problem += pulp.lpSum([x_c_I[i] * isolate_central[i] + x_c_S[i] * scan_central[i] for i in range(N)]) <= max_central
problem += pulp.lpSum([x_d_I[i] * isolate_distributed[i] + x_d_S[i] * scan_distributed[i] for i in range(N)]) <= max_distributed

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')