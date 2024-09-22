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

# Unpacking data
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(central_isolate)  # Number of clusters

# Problem
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Decision variables
x_isolate_central = pulp.LpVariable.dicts("x_isolate_central", range(N), 0, 1, pulp.LpBinary)
x_isolate_distributed = pulp.LpVariable.dicts("x_isolate_distributed", range(N), 0, 1, pulp.LpBinary)
x_scan_central = pulp.LpVariable.dicts("x_scan_central", range(N), 0, 1, pulp.LpBinary)
x_scan_distributed = pulp.LpVariable.dicts("x_scan_distributed", range(N), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(
    central_cost * (central_isolate[i] * x_isolate_central[i] + central_scan[i] * x_scan_central[i]) +
    distributed_cost * (distributed_isolate[i] * x_isolate_distributed[i] + distributed_scan[i] * x_scan_distributed[i])
    for i in range(N)
)

# Constraints
# Processing Time Constraints
problem += pulp.lpSum(central_isolate[i] * x_isolate_central[i] + central_scan[i] * x_scan_central[i] for i in range(N)) <= max_central
problem += pulp.lpSum(distributed_isolate[i] * x_isolate_distributed[i] + distributed_scan[i] * x_scan_distributed[i] for i in range(N)) <= max_distributed

# Intervention Assignment Constraints
for i in range(N):
    problem += (
        x_isolate_central[i] + x_isolate_distributed[i] +
        x_scan_central[i] + x_scan_distributed[i] == 1
    )

# Solve problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')