import pulp
import json

# Data from JSON format
data = {
    'processing_times': {
        'central': {
            'isolate': [10, 6, 8],
            'scan': [6, 4, 6]
        },
        'distributed': {
            'isolate': [12, 9, 12],
            'scan': [18, 10, 15]
        }
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

N = len(data['processing_times']['central']['isolate'])  # Number of clusters

# Create a linear programming problem
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Decision Variables
x_central_isolate = [pulp.LpVariable(f"x_central_isolate_{i}", cat='Binary') for i in range(N)]
x_central_scan = [pulp.LpVariable(f"x_central_scan_{i}", cat='Binary') for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f"x_distributed_isolate_{i}", cat='Binary') for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f"x_distributed_scan_{i}", cat='Binary') for i in range(N)]

# Objective Function
problem += pulp.lpSum([
    data['costs']['central'] * (x_central_isolate[i] * data['processing_times']['central']['isolate'][i] + 
                                 x_central_scan[i] * data['processing_times']['central']['scan'][i])
    + data['costs']['distributed'] * (x_distributed_isolate[i] * data['processing_times']['distributed']['isolate'][i] + 
                                       x_distributed_scan[i] * data['processing_times']['distributed']['scan'][i])
    for i in range(N)
]), "Total_Cost"

# Constraints
for i in range(N):
    problem += (x_central_isolate[i] + x_central_scan[i] + 
                 x_distributed_isolate[i] + x_distributed_scan[i] == 1, 
                 f"One_Intervention_Type_{i}")

problem += (pulp.lpSum([
    x_central_isolate[i] * data['processing_times']['central']['isolate'][i] + 
    x_central_scan[i] * data['processing_times']['central']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['central_max_hours'], 
"Max_Central_Hours")

problem += (pulp.lpSum([
    x_distributed_isolate[i] * data['processing_times']['distributed']['isolate'][i] + 
    x_distributed_scan[i] * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
]) <= data['max_hours']['distributed_max_hours'], 
"Max_Distributed_Hours")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')