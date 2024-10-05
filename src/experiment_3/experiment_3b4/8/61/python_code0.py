import pulp

# Data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Parameters
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Problem
problem = pulp.LpProblem("Network_Intervention_Problem", pulp.LpMinimize)

# Decision Variables
x_vars = {(i, j, k): pulp.LpVariable(f"x_{i}_{j}_{k}", cat='Binary')
          for i in range(N)
          for j in ['isolate', 'scan']
          for k in ['central', 'distributed']}

# Objective Function
problem += pulp.lpSum(
    central_cost * (isolate_central[i] * x_vars[i, 'isolate', 'central'] + scan_central[i] * x_vars[i, 'scan', 'central']) +
    distributed_cost * (isolate_distributed[i] * x_vars[i, 'isolate', 'distributed'] + scan_distributed[i] * x_vars[i, 'scan', 'distributed'])
    for i in range(N)
)

# Constraints
# Each cluster must be treated with one intervention type and one processing method
for i in range(N):
    problem += (x_vars[i, 'isolate', 'central'] + x_vars[i, 'scan', 'central'] +
                x_vars[i, 'isolate', 'distributed'] + x_vars[i, 'scan', 'distributed'] == 1)

# Central processing time limit
problem += pulp.lpSum(isolate_central[i] * x_vars[i, 'isolate', 'central'] + scan_central[i] * x_vars[i, 'scan', 'central'] for i in range(N)) <= max_central

# Distributed processing time limit
problem += pulp.lpSum(isolate_distributed[i] * x_vars[i, 'isolate', 'distributed'] + scan_distributed[i] * x_vars[i, 'scan', 'distributed'] for i in range(N)) <= max_distributed

# Solve
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')