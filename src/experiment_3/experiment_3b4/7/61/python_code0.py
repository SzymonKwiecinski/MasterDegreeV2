import pulp

# Data from JSON
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Unpack data
p_central_isolate = data['processing_times']['central']['isolate']
p_central_scan = data['processing_times']['central']['scan']
p_distributed_isolate = data['processing_times']['distributed']['isolate']
p_distributed_scan = data['processing_times']['distributed']['scan']

c_central = data['costs']['central']
c_distributed = data['costs']['distributed']

h_max_central = data['max_hours']['central_max_hours']
h_max_distributed = data['max_hours']['distributed_max_hours']

N = range(len(p_central_isolate))  # Set of clusters

# Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Variables
x_central_isolate = pulp.LpVariable.dicts("x_central_isolate", N, cat='Binary')
x_central_scan = pulp.LpVariable.dicts("x_central_scan", N, cat='Binary')
x_distributed_isolate = pulp.LpVariable.dicts("x_distributed_isolate", N, cat='Binary')
x_distributed_scan = pulp.LpVariable.dicts("x_distributed_scan", N, cat='Binary')

# Objective Function
problem += pulp.lpSum([
    c_central * (p_central_isolate[i] * x_central_isolate[i] + p_central_scan[i] * x_central_scan[i]) +
    c_distributed * (p_distributed_isolate[i] * x_distributed_isolate[i] + p_distributed_scan[i] * x_distributed_scan[i])
    for i in N
])

# Constraints
for i in N:
    problem += (x_central_isolate[i] + x_central_scan[i] +
                x_distributed_isolate[i] + x_distributed_scan[i] == 1)

problem += pulp.lpSum([p_central_isolate[i] * x_central_isolate[i] + p_central_scan[i] * x_central_scan[i] for i in N]) <= h_max_central

problem += pulp.lpSum([p_distributed_isolate[i] * x_distributed_isolate[i] + p_distributed_scan[i] * x_distributed_scan[i] for i in N]) <= h_max_distributed

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')