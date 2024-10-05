import pulp

# Data input
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

N = len(isolate_central)

# Create problem
problem = pulp.LpProblem("Intrusion Response Optimization", pulp.LpMinimize)

# Decision variables: binary for each intervention type and method
x_ij = {(i, j, k): pulp.LpVariable(f'x_{i}_{j}_{k}', cat='Binary') 
        for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']}

# Objective function
problem += pulp.lpSum(
    (isolate_central[i] * x_ij[(i, 'isolate', 'central')] + scan_central[i] * x_ij[(i, 'scan', 'central')]) * central_cost +
    (isolate_distributed[i] * x_ij[(i, 'isolate', 'distributed')] + scan_distributed[i] * x_ij[(i, 'scan', 'distributed')]) * distributed_cost
    for i in range(N)
)

# Constraints
# Each cluster should be treated with one intervention type in one method
for i in range(N):
    problem += pulp.lpSum(x_ij[(i, j, k)] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) == 1

# Maximum hour constraints for central and distributed methods
problem += pulp.lpSum(
    isolate_central[i] * x_ij[(i, 'isolate', 'central')] + scan_central[i] * x_ij[(i, 'scan', 'central')]
    for i in range(N)
) <= max_central

problem += pulp.lpSum(
    isolate_distributed[i] * x_ij[(i, 'isolate', 'distributed')] + scan_distributed[i] * x_ij[(i, 'scan', 'distributed')]
    for i in range(N)
) <= max_distributed

# Solve the problem
problem.solve()

# Extract the solutions
interventions = []
total_cost = 0
for i in range(N):
    for j in ['isolate', 'scan']:
        for k in ['central', 'distributed']:
            if pulp.value(x_ij[(i, j, k)]) == 1:
                amount = isolate_central[i] if j == 'isolate' else scan_central[i]
                if k == 'distributed':
                    amount = isolate_distributed[i] if j == 'isolate' else scan_distributed[i]
                cost = amount * (central_cost if k == 'central' else distributed_cost)
                interventions.append({
                    "cluster_id": i + 1,
                    "type": j,
                    "method": k,
                    "amount": amount
                })
                total_cost += cost

# Output
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')