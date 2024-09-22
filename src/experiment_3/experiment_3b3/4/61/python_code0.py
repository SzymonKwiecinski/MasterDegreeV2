import pulp

# Data
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

# Problem setup
problem = pulp.LpProblem("Intervention_Cost_Minimization", pulp.LpMinimize)
N = len(data['processing_times']['central']['isolate'])

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in [1, 2] for k in [1, 2]), 
                          cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum(
    data['costs']['central'] * data['processing_times']['central']['isolate'][i] * x[i, 1, 1] + 
    data['costs']['central'] * data['processing_times']['central']['scan'][i] * x[i, 2, 1] + 
    data['costs']['distributed'] * data['processing_times']['distributed']['isolate'][i] * x[i, 1, 2] + 
    data['costs']['distributed'] * data['processing_times']['distributed']['scan'][i] * x[i, 2, 2]
    for i in range(N)
)

# Constraints
# Each cluster has one intervention type
for i in range(N):
    problem += pulp.lpSum(x[i, j, k] for j in [1, 2] for k in [1, 2]) == 1

# Central processing time constraint
problem += pulp.lpSum(
    data['processing_times']['central']['isolate'][i] * x[i, 1, 1] + 
    data['processing_times']['central']['scan'][i] * x[i, 2, 1]
    for i in range(N)
) <= data['max_hours']['central_max_hours']

# Distributed processing time constraint
problem += pulp.lpSum(
    data['processing_times']['distributed']['isolate'][i] * x[i, 1, 2] + 
    data['processing_times']['distributed']['scan'][i] * x[i, 2, 2]
    for i in range(N)
) <= data['max_hours']['distributed_max_hours']

# Solve the problem
problem.solve()

# Print the outputs
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')