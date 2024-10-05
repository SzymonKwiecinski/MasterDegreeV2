import pulp

# Input data
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

# Unpacking the data
processing_times = data['processing_times']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(processing_times['central']['isolate'])

# Sets
clusters = range(N)
intervention_types = ['isolate', 'scan']
processing_methods = ['central', 'distributed']

# Initialize the problem
problem = pulp.LpProblem("Network_Intrusion_Intervention", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (clusters, intervention_types, processing_methods), 0, 1, pulp.LpBinary)
amount = pulp.LpVariable.dicts("amount", clusters, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    [amount[i] * (x[i][t][m] * central_cost if m == 'central' else x[i][t][m] * distributed_cost)
     for i in clusters for t in intervention_types for m in processing_methods]
)

# Constraints
# Each cluster must have exactly one intervention type and processing method
for i in clusters:
    problem += pulp.lpSum([x[i][t][m] for t in intervention_types for m in processing_methods]) == 1

# Central processing time constraint
problem += pulp.lpSum(
    [amount[i] * processing_times['central'][t][i] * x[i][t]['central'] for i in clusters for t in intervention_types]
) <= max_central

# Distributed processing time constraint
problem += pulp.lpSum(
    [amount[i] * processing_times['distributed'][t][i] * x[i][t]['distributed'] for i in clusters for t in intervention_types]
) <= max_distributed

# Solve the problem
problem.solve()

# Prepare the output
output = {'interventions': [], 'total_cost': pulp.value(problem.objective)}

for i in clusters:
    for t in intervention_types:
        for m in processing_methods:
            if pulp.value(x[i][t][m]) == 1:
                output['interventions'].append({
                    'cluster_id': i + 1,
                    'type': t,
                    'method': m,
                    'amount': pulp.value(amount[i])
                })

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')