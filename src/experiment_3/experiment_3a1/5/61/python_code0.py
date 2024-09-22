import pulp

# Data parsing
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70}, 
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

N = len(data['processing_times']['central']['isolate'])

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", 
                           ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), 
                           cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['costs']['central'] * pulp.lpSum(
        x[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] + 
        x[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i] 
        for i in range(N)
    ) + 
    data['costs']['distributed'] * pulp.lpSum(
        x[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] + 
        x[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i] 
        for i in range(N)
    )
)

# Constraints

# 1. Each cluster is assigned exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# 2. Central processing time constraint
problem += pulp.lpSum(
    x[i, 'isolate', 'central'] * data['processing_times']['central']['isolate'][i] + 
    x[i, 'scan', 'central'] * data['processing_times']['central']['scan'][i] 
    for i in range(N)
) <= data['max_hours']['central_max_hours']

# 3. Distributed processing time constraint
problem += pulp.lpSum(
    x[i, 'isolate', 'distributed'] * data['processing_times']['distributed']['isolate'][i] + 
    x[i, 'scan', 'distributed'] * data['processing_times']['distributed']['scan'][i] 
    for i in range(N)
) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')