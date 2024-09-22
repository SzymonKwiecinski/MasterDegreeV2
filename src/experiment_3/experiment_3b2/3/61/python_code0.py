import pulp

# Data extraction
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

N = len(data['processing_times']['central']['isolate'])

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), cat='Binary')

# Objective function
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

problem += pulp.lpSum(
    central_cost * pulp.lpSum(x[i, j, 'central'] * data['processing_times']['central'][j][i] for j in ['isolate', 'scan']) +
    distributed_cost * pulp.lpSum(x[i, j, 'distributed'] * data['processing_times']['distributed'][j][i] for j in ['isolate', 'scan'])
    for i in range(N)
)

# Constraints
# Each cluster must have exactly one intervention type
for i in range(N):
    problem += pulp.lpSum(x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# Total central processing time must not exceed the central maximum hours
problem += pulp.lpSum(
    pulp.lpSum(x[i, j, 'central'] * data['processing_times']['central'][j][i] for j in ['isolate', 'scan'])
    for i in range(N)
) <= data['max_hours']['central_max_hours']

# Total distributed processing time must not exceed the distributed maximum hours
problem += pulp.lpSum(
    pulp.lpSum(x[i, j, 'distributed'] * data['processing_times']['distributed'][j][i] for j in ['isolate', 'scan'])
    for i in range(N)
) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')