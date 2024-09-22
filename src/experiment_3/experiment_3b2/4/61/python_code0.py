import pulp

# Data from JSON format
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extract data from the dictionary
N = len(data['processing_times']['central']['isolate'])
t_central = data['processing_times']['central']
t_distributed = data['processing_times']['distributed']
c_central = data['costs']['central']
c_distributed = data['costs']['distributed']
H_central_max = data['max_hours']['central_max_hours']
H_distributed_max = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, 'central') for i in range(N) for j in t_central), cat='Binary')
y = pulp.LpVariable.dicts("y", ((i, j, 'distributed') for i in range(N) for j in t_distributed), cat='Binary')

# Objective function
problem += pulp.lpSum(c_central * t_central[j][i] * x[i, j, 'central'] for i in range(N) for j in t_central) + \
            pulp.lpSum(c_distributed * t_distributed[j][i] * y[i, j, 'distributed'] for i in range(N) for j in t_distributed)

# Constraints

# Each cluster uses one intervention
for i in range(N):
    problem += pulp.lpSum(x[i, j, 'central'] for j in t_central) + pulp.lpSum(y[i, j, 'distributed'] for j in t_distributed) == 1

# Central processing time limit
problem += pulp.lpSum(t_central[j][i] * x[i, j, 'central'] for i in range(N) for j in t_central) <= H_central_max

# Distributed processing time limit
problem += pulp.lpSum(t_distributed[j][i] * y[i, j, 'distributed'] for i in range(N) for j in t_distributed) <= H_distributed_max

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')