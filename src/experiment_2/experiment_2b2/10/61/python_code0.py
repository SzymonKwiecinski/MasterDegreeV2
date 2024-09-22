import pulp

# Load data
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

# Define clusters
N = len(data['processing_times']['central']['isolate'])

# Define the problem
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Isolate_Central", (range(N)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("Scan_Central", (range(N)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("Isolate_Distributed", (range(N)), lowBound=0, cat='Continuous')
w = pulp.LpVariable.dicts("Scan_Distributed", (range(N)), lowBound=0, cat='Continuous')

# Objective function
problem += (
    pulp.lpSum(data['costs']['central'] * (x[i] + y[i]) for i in range(N)) +
    pulp.lpSum(data['costs']['distributed'] * (z[i] + w[i]) for i in range(N))
)

# Constraints
# Central processing hours
problem += pulp.lpSum(data['processing_times']['central']['isolate'][i] * x[i] + 
                      data['processing_times']['central']['scan'][i] * y[i] for i in range(N)) <= data['max_hours']['central_max_hours']

# Distributed processing hours
problem += pulp.lpSum(data['processing_times']['distributed']['isolate'][i] * z[i] + 
                      data['processing_times']['distributed']['scan'][i] * w[i] for i in range(N)) <= data['max_hours']['distributed_max_hours']

# Each cluster must choose exactly one intervention type
for i in range(N):
    problem += x[i] + y[i] + z[i] + w[i] == 1

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in range(N):
    if pulp.value(x[i]) > 0:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": pulp.value(x[i])})
    elif pulp.value(y[i]) > 0:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": pulp.value(y[i])})
    elif pulp.value(z[i]) > 0:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": pulp.value(z[i])})
    elif pulp.value(w[i]) > 0:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": pulp.value(w[i])})

total_cost = pulp.value(problem.objective)

# Output format
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')