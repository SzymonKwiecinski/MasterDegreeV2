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

# Parameters
N = len(data['processing_times']['central']['isolate'])
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Problem
problem = pulp.LpProblem("Intrusion_Intervention_Minimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']), cat='Binary')

# Objective Function
total_cost = sum(
    x[i, j, k] * (central_cost if k == 'central' else distributed_cost) * (
        data['processing_times'][k][j][i]
    ) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']
)
problem += total_cost

# Constraints
# 1. Each cluster must have exactly one intervention type
for i in range(N):
    problem += sum(x[i, j, k] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# 2. Central processing time constraint
problem += sum(
    x[i, j, 'central'] * data['processing_times']['central'][j][i] for i in range(N) for j in ['isolate', 'scan']
) <= max_central

# 3. Distributed processing time constraint
problem += sum(
    x[i, j, 'distributed'] * data['processing_times']['distributed'][j][i] for i in range(N) for j in ['isolate', 'scan']
) <= max_distributed

# Solve
problem.solve()

# Output
interventions = []
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(x[i, j, k]) == 1:
                interventions.append({
                    "cluster_id": i,
                    "type": j,
                    "method": k,
                    "amount": pulp.value(x[i, j, k])
                })

result = {
    "interventions": interventions,
    "total_cost": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(result)