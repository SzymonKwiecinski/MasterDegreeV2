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

# Constants
M = 1000  # Large constant for constraint

# Unpack data
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Number of clusters
N = len(isolate_central)

# Define Problem
problem = pulp.LpProblem("Cluster_Intervention_Problem", pulp.LpMinimize)

# Decision Variables
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

x_isolate_central = pulp.LpVariable.dicts("x_isolate_central", range(N), lowBound=0)
x_scan_central = pulp.LpVariable.dicts("x_scan_central", range(N), lowBound=0)
x_isolate_distributed = pulp.LpVariable.dicts("x_isolate_distributed", range(N), lowBound=0)
x_scan_distributed = pulp.LpVariable.dicts("x_scan_distributed", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum([
    central_cost * (x_isolate_central[i] + x_scan_central[i]) +
    distributed_cost * (x_isolate_distributed[i] + x_scan_distributed[i])
    for i in range(N)
])

# Constraints

# Time Constraints for Central Processing
problem += pulp.lpSum([x_isolate_central[i] + x_scan_central[i] for i in range(N)]) <= max_central

# Time Constraints for Distributed Processing
problem += pulp.lpSum([x_isolate_distributed[i] + x_scan_distributed[i] for i in range(N)]) <= max_distributed

# Ensure that only one intervention type is chosen per cluster
for i in range(N):
    problem += (
        x_isolate_central[i] + x_scan_central[i] +
        x_isolate_distributed[i] + x_scan_distributed[i] <= M * y[i]
    )
    
# Processing time limits for each intervention type
for i in range(N):
    problem += x_isolate_central[i] <= isolate_central[i] * y[i]
    problem += x_scan_central[i] <= scan_central[i] * y[i]
    problem += x_isolate_distributed[i] <= isolate_distributed[i] * y[i]
    problem += x_scan_distributed[i] <= scan_distributed[i] * y[i]

# Solve the problem
problem.solve()

# Output
results = []
for i in range(N):
    for j, process in enumerate(['isolate', 'scan']):
        for k, method in enumerate(['central', 'distributed']):
            var_name = f"x_{process}_{method}[{i}]"
            var_value = pulp.value(locals()[var_name])
            if var_value > 0:
                results.append({
                    'cluster_id': i,
                    'type': process,
                    'method': method,
                    'amount': var_value
                })

# Print results
for result in results:
    print(result)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')