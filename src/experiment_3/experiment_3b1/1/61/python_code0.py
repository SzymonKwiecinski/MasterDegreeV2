import pulp
import json

# Data provided in JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extract data
processing_times = data['processing_times']
costs = data['costs']
max_hours = data['max_hours']

N = len(processing_times['central']['isolate'])

# Create a linear programming problem
problem = pulp.LpProblem("Intervention_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), ['isolate', 'scan'], ['central', 'distributed']), cat='Binary')

# Objective function
problem += pulp.lpSum(
    (costs['central'] * (processing_times['central']['isolate'][i] * x[i]['isolate']['central'] +
                         processing_times['central']['scan'][i] * x[i]['scan']['central']) +
     costs['distributed'] * (processing_times['distributed']['isolate'][i] * x[i]['isolate']['distributed'] +
                             processing_times['distributed']['scan'][i] * x[i]['scan']['distributed']))
    for i in range(N)
)

# Constraints
# Each cluster must be treated with one intervention type
for i in range(N):
    problem += pulp.lpSum(x[i][j][k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# Central processing time constraint
problem += pulp.lpSum(
    (processing_times['central']['isolate'][i] * x[i]['isolate']['central'] +
     processing_times['central']['scan'][i] * x[i]['scan']['central'])
    for i in range(N)
) <= max_hours['central_max_hours']

# Distributed processing time constraint
problem += pulp.lpSum(
    (processing_times['distributed']['isolate'][i] * x[i]['isolate']['distributed'] +
     processing_times['distributed']['scan'][i] * x[i]['scan']['distributed'])
    for i in range(N)
) <= max_hours['distributed_max_hours']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')