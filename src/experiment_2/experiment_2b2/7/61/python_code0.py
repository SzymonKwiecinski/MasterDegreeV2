import pulp

# Load the data from the JSON
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

# Extract the necessary data
central_isolate = data['processing_times']['central']['isolate']
central_scan = data['processing_times']['central']['scan']
distributed_isolate = data['processing_times']['distributed']['isolate']
distributed_scan = data['processing_times']['distributed']['scan']

central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']

max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

num_clusters = len(central_isolate)

# Define the problem
problem = pulp.LpProblem("Network_Intervention_Strategy", pulp.LpMinimize)

# Decision variables
x_ci = [pulp.LpVariable(f'x_ci_{i}', cat='Binary') for i in range(num_clusters)]
x_cs = [pulp.LpVariable(f'x_cs_{i}', cat='Binary') for i in range(num_clusters)]
x_di = [pulp.LpVariable(f'x_di_{i}', cat='Binary') for i in range(num_clusters)]
x_ds = [pulp.LpVariable(f'x_ds_{i}', cat='Binary') for i in range(num_clusters)]

# Objective Function
problem += pulp.lpSum(
    [central_cost * (central_isolate[i] * x_ci[i] + central_scan[i] * x_cs[i]) +
     distributed_cost * (distributed_isolate[i] * x_di[i] + distributed_scan[i] * x_ds[i])
     for i in range(num_clusters)]
)

# Constraints
for i in range(num_clusters):
    problem += x_ci[i] + x_cs[i] + x_di[i] + x_ds[i] == 1

problem += pulp.lpSum([central_isolate[i] * x_ci[i] + central_scan[i] * x_cs[i]
                       for i in range(num_clusters)]) <= max_central

problem += pulp.lpSum([distributed_isolate[i] * x_di[i] + distributed_scan[i] * x_ds[i]
                       for i in range(num_clusters)]) <= max_distributed

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in range(num_clusters):
    if x_ci[i].varValue == 1:
        interventions.append({
            "cluster_id": i + 1,
            "type": "isolate",
            "method": "central",
            "amount": central_isolate[i]
        })
    elif x_cs[i].varValue == 1:
        interventions.append({
            "cluster_id": i + 1,
            "type": "scan",
            "method": "central",
            "amount": central_scan[i]
        })
    elif x_di[i].varValue == 1:
        interventions.append({
            "cluster_id": i + 1,
            "type": "isolate",
            "method": "distributed",
            "amount": distributed_isolate[i]
        })
    elif x_ds[i].varValue == 1:
        interventions.append({
            "cluster_id": i + 1,
            "type": "scan",
            "method": "distributed",
            "amount": distributed_scan[i]
        })

total_cost = pulp.value(problem.objective)

output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')