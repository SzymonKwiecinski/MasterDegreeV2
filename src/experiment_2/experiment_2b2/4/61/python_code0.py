import pulp

# Define data from JSON
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

# Extracting information
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

processing_times = data['processing_times']

N = len(processing_times['central']['isolate'])

# Define problem
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Decision variables
x_isolate_central = [pulp.LpVariable(f"x_isolate_central_{i}", cat='Binary') for i in range(N)]
x_scan_central = [pulp.LpVariable(f"x_scan_central_{i}", cat='Binary') for i in range(N)]
x_isolate_distributed = [pulp.LpVariable(f"x_isolate_distributed_{i}", cat='Binary') for i in range(N)]
x_scan_distributed = [pulp.LpVariable(f"x_scan_distributed_{i}", cat='Binary') for i in range(N)]

# Objective function
problem += (
    pulp.lpSum([x_isolate_central[i] * processing_times['central']['isolate'][i] * central_cost
                for i in range(N)]) +
    pulp.lpSum([x_scan_central[i] * processing_times['central']['scan'][i] * central_cost
                for i in range(N)]) +
    pulp.lpSum([x_isolate_distributed[i] * processing_times['distributed']['isolate'][i] * distributed_cost
                for i in range(N)]) +
    pulp.lpSum([x_scan_distributed[i] * processing_times['distributed']['scan'][i] * distributed_cost
                for i in range(N)])
)

# Constraints
for i in range(N):
    problem += x_isolate_central[i] + x_scan_central[i] + x_isolate_distributed[i] + x_scan_distributed[i] == 1

problem += pulp.lpSum([x_isolate_central[i] * processing_times['central']['isolate'][i]
                       for i in range(N)]) + pulp.lpSum([x_scan_central[i] * processing_times['central']['scan'][i]
                       for i in range(N)]) <= max_central

problem += pulp.lpSum([x_isolate_distributed[i] * processing_times['distributed']['isolate'][i]
                       for i in range(N)]) + pulp.lpSum([x_scan_distributed[i] * processing_times['distributed']['scan'][i]
                       for i in range(N)]) <= max_distributed

# Solving problem
problem.solve()

# Output
interventions = []
for i in range(N):
    if pulp.value(x_isolate_central[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": processing_times['central']['isolate'][i]})
    elif pulp.value(x_scan_central[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": processing_times['central']['scan'][i]})
    elif pulp.value(x_isolate_distributed[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": processing_times['distributed']['isolate'][i]})
    elif pulp.value(x_scan_distributed[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": processing_times['distributed']['scan'][i]})

total_cost = pulp.value(problem.objective)

# Result
result = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')