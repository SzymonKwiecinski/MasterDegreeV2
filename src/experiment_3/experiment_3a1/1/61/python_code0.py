import pulp
import json

# Load data
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extract parameters from data
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Network_Interventions", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(N) for j in range(2) for k in range(2)), cat='Binary')
amount = pulp.LpVariable.dicts("amount", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    (central_cost * amount[i] * x[i, 0, 0] + 
    distributed_cost * amount[i] * x[i, 0, 1] +
    central_cost * amount[i] * x[i, 1, 0] + 
    distributed_cost * amount[i] * x[i, 1, 1])
    for i in range(N)
)

# Constraints
for i in range(N):
    problem += pulp.lpSum(amount[i] * x[i, j, k] for j in range(2) for k in range(2)) <= max_central
    problem += pulp.lpSum(amount[i] * x[i, j, k] for j in range(2) for k in range(2)) <= max_distributed

for i in range(N):
    problem += pulp.lpSum(x[i, j, k] for j in range(2) for k in range(2)) == 1

for i in range(N):
    problem += amount[i] == (isolate_central[i] * x[i, 0, 0] + 
                              scan_central[i] * x[i, 1, 0] + 
                              isolate_distributed[i] * x[i, 0, 1] + 
                              scan_distributed[i] * x[i, 1, 1])

# Solve the problem
problem.solve()

# Output the interventions and total cost
interventions = []
for i in range(N):
    for j in range(2):
        for k in range(2):
            if pulp.value(x[i, j, k]) == 1:
                interventions.append({
                    "cluster_id": i + 1,
                    "type": "isolate" if j == 0 else "scan",
                    "method": "central" if k == 0 else "distributed",
                    "amount": pulp.value(amount[i])
                })

output = {
    "interventions": interventions,
    "total_cost": pulp.value(problem.objective)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')