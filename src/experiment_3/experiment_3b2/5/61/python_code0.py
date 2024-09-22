import pulp
import json

# Data from the provided JSON format
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

# Extracting data
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
C_c = data['costs']['central']
C_d = data['costs']['distributed']
H_c = data['max_hours']['central_max_hours']
H_d = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Variables
x_c_I = [pulp.LpVariable(f'x_{i}_c_I', cat='Binary') for i in range(N)]
x_c_S = [pulp.LpVariable(f'x_{i}_c_S', cat='Binary') for i in range(N)]
x_d_I = [pulp.LpVariable(f'x_{i}_d_I', cat='Binary') for i in range(N)]
x_d_S = [pulp.LpVariable(f'x_{i}_d_S', cat='Binary') for i in range(N)]

# Objective Function
problem += pulp.lpSum([
    x_c_I[i] * isolate_central[i] * C_c + 
    x_c_S[i] * scan_central[i] * C_c + 
    x_d_I[i] * isolate_distributed[i] * C_d + 
    x_d_S[i] * scan_distributed[i] * C_d for i in range(N)
])

# Constraints
problem += pulp.lpSum([x_c_I[i] * isolate_central[i] + x_c_S[i] * scan_central[i] for i in range(N)]) <= H_c
problem += pulp.lpSum([x_d_I[i] * isolate_distributed[i] + x_d_S[i] * scan_distributed[i] for i in range(N)]) <= H_d
for i in range(N):
    problem += x_c_I[i] + x_c_S[i] + x_d_I[i] + x_d_S[i] == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')