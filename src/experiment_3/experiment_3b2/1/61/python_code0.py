import pulp
import json

# Data provided in JSON format
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
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Decision Variables
x_c = pulp.LpVariable.dicts('x_c', range(N), cat='Binary')  # Isolate with central
x_d = pulp.LpVariable.dicts('x_d', range(N), cat='Binary')  # Isolate with distributed
y_c = pulp.LpVariable.dicts('y_c', range(N), cat='Binary')  # Scan with central
y_d = pulp.LpVariable.dicts('y_d', range(N), cat='Binary')  # Scan with distributed

# Initialize the problem
problem = pulp.LpProblem("Network_Intrusion_Intervention_Optimization", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum([central_cost * (x_c[i] * data['processing_times']['central']['isolate'][i] + y_c[i] * data['processing_times']['central']['scan'][i]) +
                        distributed_cost * (x_d[i] * data['processing_times']['distributed']['isolate'][i] + y_d[i] * data['processing_times']['distributed']['scan'][i])
                        for i in range(N)])

# Constraints
# Each cluster must have exactly one type of intervention
for i in range(N):
    problem += (x_c[i] + x_d[i] + y_c[i] + y_d[i] == 1)

# Central processing must not exceed the maximum allotted hours
problem += (pulp.lpSum([x_c[i] * data['processing_times']['central']['isolate'][i] + y_c[i] * data['processing_times']['central']['scan'][i] for i in range(N)]) <= max_central)

# Distributed processing must not exceed the maximum allotted hours
problem += (pulp.lpSum([x_d[i] * data['processing_times']['distributed']['isolate'][i] + y_d[i] * data['processing_times']['distributed']['scan'][i] for i in range(N)]) <= max_distributed)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')