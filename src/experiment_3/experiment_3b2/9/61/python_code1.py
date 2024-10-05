import pulp

# Data from JSON
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

# Constants
N = len(data['processing_times']['central']['isolate'])

# Create the problem variable
problem = pulp.LpProblem("Network_Intrusion_Response", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (i for i in range(N)), cat='Binary')  # 0: central, 1: distributed
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')  # 0: isolate, 1: scan

# Objective Function
problem += pulp.lpSum(
    [
        x[i] * (y[i] * data['processing_times']['central']['isolate'][i] + (1 - y[i]) * data['processing_times']['central']['scan'][i]) * data['costs']['central'] +
        (1 - x[i]) * (y[i] * data['processing_times']['distributed']['isolate'][i] + (1 - y[i]) * data['processing_times']['distributed']['scan'][i]) * data['costs']['distributed']
        for i in range(N)
    ]
)

# Constraints
problem += pulp.lpSum(
    [x[i] * (y[i] * data['processing_times']['central']['isolate'][i] + (1 - y[i]) * data['processing_times']['central']['scan'][i]) for i in range(N)]
) <= data['max_hours']['central_max_hours']

problem += pulp.lpSum(
    [(1 - x[i]) * (y[i] * data['processing_times']['distributed']['isolate'][i] + (1 - y[i]) * data['processing_times']['distributed']['scan'][i]) for i in range(N)]
) <= data['max_hours']['distributed_max_hours']

for i in range(N):
    problem += x[i] + (1 - x[i]) == 1  # Either central or distributed processing
    problem += y[i] + (1 - y[i]) == 1  # Either isolate or scan

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')