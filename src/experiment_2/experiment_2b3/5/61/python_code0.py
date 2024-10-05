import pulp

# Data from the JSON
data = {
    "processing_times": {
        "central": {
            "isolate": [10, 6, 8],
            "scan": [6, 4, 6]
        },
        "distributed": {
            "isolate": [12, 9, 12],
            "scan": [18, 10, 15]
        }
    },
    "costs": {
        "central": 150,
        "distributed": 70
    },
    "max_hours": {
        "central_max_hours": 16,
        "distributed_max_hours": 33
    }
}

N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']
processing_times = data['processing_times']

# Creating the LP problem
problem = pulp.LpProblem("NetworkIntervention", pulp.LpMinimize)

# Decision variables
x_isolate_central = pulp.LpVariable.dicts("x_isolate_central", range(N), lowBound=0, cat='Binary')
x_scan_central = pulp.LpVariable.dicts("x_scan_central", range(N), lowBound=0, cat='Binary')
x_isolate_distributed = pulp.LpVariable.dicts("x_isolate_distributed", range(N), lowBound=0, cat='Binary')
x_scan_distributed = pulp.LpVariable.dicts("x_scan_distributed", range(N), lowBound=0, cat='Binary')

# Objective function
problem += pulp.lpSum([
    central_cost * (x_isolate_central[i] * processing_times['central']['isolate'][i] + 
                    x_scan_central[i] * processing_times['central']['scan'][i]) +
    distributed_cost * (x_isolate_distributed[i] * processing_times['distributed']['isolate'][i] + 
                        x_scan_distributed[i] * processing_times['distributed']['scan'][i])
    for i in range(N)
])

# Constraints
for i in range(N):
    # Only one type of intervention should be chosen for each cluster
    problem += (x_isolate_central[i] + x_scan_central[i] + 
                x_isolate_distributed[i] + x_scan_distributed[i]) == 1
    
# Maximum hours limitation
problem += pulp.lpSum([
    x_isolate_central[i] * processing_times['central']['isolate'][i] +
    x_scan_central[i] * processing_times['central']['scan'][i]
    for i in range(N)
]) <= max_central

problem += pulp.lpSum([
    x_isolate_distributed[i] * processing_times['distributed']['isolate'][i] +
    x_scan_distributed[i] * processing_times['distributed']['scan'][i]
    for i in range(N)
]) <= max_distributed

# Solve the problem
problem.solve()

# Gather the results
interventions = []
for i in range(N):
    if pulp.value(x_isolate_central[i]) == 1:
        interventions.append({
            "cluster_id": i,
            "type": "isolate",
            "method": "central",
            "amount": processing_times['central']['isolate'][i]
        })
    elif pulp.value(x_scan_central[i]) == 1:
        interventions.append({
            "cluster_id": i,
            "type": "scan",
            "method": "central",
            "amount": processing_times['central']['scan'][i]
        })
    elif pulp.value(x_isolate_distributed[i]) == 1:
        interventions.append({
            "cluster_id": i,
            "type": "isolate",
            "method": "distributed",
            "amount": processing_times['distributed']['isolate'][i]
        })
    elif pulp.value(x_scan_distributed[i]) == 1:
        interventions.append({
            "cluster_id": i,
            "type": "scan",
            "method": "distributed",
            "amount": processing_times['distributed']['scan'][i]
        })

total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

# Print the output
print(output)
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")