import pulp

# Data provided
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

# Variables
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Setup the problem
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Intervention",
                          [(i, method, intervention) for i in range(N) for method in ['central', 'distributed'] for intervention in ['isolate', 'scan']],
                          cat='Binary')

# Objective Function: Minimize the total cost
problem += pulp.lpSum([
    x[(i, 'central', 'isolate')] * data['processing_times']['central']['isolate'][i] * central_cost +
    x[(i, 'central', 'scan')] * data['processing_times']['central']['scan'][i] * central_cost +
    x[(i, 'distributed', 'isolate')] * data['processing_times']['distributed']['isolate'][i] * distributed_cost +
    x[(i, 'distributed', 'scan')] * data['processing_times']['distributed']['scan'][i] * distributed_cost
    for i in range(N)
])

# Constraints
# Each cluster must have exactly one type of intervention and method
for i in range(N):
    problem += pulp.lpSum([x[(i, method, intervention)] for method in ['central', 'distributed'] for intervention in ['isolate', 'scan']]) == 1

# Central processing hours limit
problem += pulp.lpSum([
    x[(i, 'central', 'isolate')] * data['processing_times']['central']['isolate'][i] +
    x[(i, 'central', 'scan')] * data['processing_times']['central']['scan'][i]
    for i in range(N)
]) <= max_central

# Distributed processing hours limit
problem += pulp.lpSum([
    x[(i, 'distributed', 'isolate')] * data['processing_times']['distributed']['isolate'][i] +
    x[(i, 'distributed', 'scan')] * data['processing_times']['distributed']['scan'][i]
    for i in range(N)
]) <= max_distributed

# Solve the problem
problem.solve()

# Output result
interventions = []
total_cost = pulp.value(problem.objective)

for i in range(N):
    for method in ['central', 'distributed']:
        for intervention in ['isolate', 'scan']:
            if pulp.value(x[(i, method, intervention)]) == 1:
                time_amount = data['processing_times'][method][intervention][i]
                interventions.append({
                    "cluster_id": i + 1,  # assuming cluster_id starts at 1
                    "type": intervention,
                    "method": method,
                    "amount": time_amount
                })

result = {
    "interventions": interventions,
    "total_cost": total_cost
}

# Output the result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')