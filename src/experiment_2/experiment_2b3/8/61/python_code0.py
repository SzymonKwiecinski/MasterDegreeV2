import pulp

# Input data
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

# Indices
N = len(data["processing_times"]["central"]["isolate"])

# Problem setup
problem = pulp.LpProblem("Network_Intervention", pulp.LpMinimize)

# Decision variables
x_central_isolate = [pulp.LpVariable(f"central_isolate_{i}", cat='Binary') for i in range(N)]
x_central_scan = [pulp.LpVariable(f"central_scan_{i}", cat='Binary') for i in range(N)]
x_distributed_isolate = [pulp.LpVariable(f"distributed_isolate_{i}", cat='Binary') for i in range(N)]
x_distributed_scan = [pulp.LpVariable(f"distributed_scan_{i}", cat='Binary') for i in range(N)]

# Objective function
total_cost = pulp.lpSum([
    x_central_isolate[i] * data["processing_times"]["central"]["isolate"][i] * data["costs"]["central"] +
    x_central_scan[i] * data["processing_times"]["central"]["scan"][i] * data["costs"]["central"] +
    x_distributed_isolate[i] * data["processing_times"]["distributed"]["isolate"][i] * data["costs"]["distributed"] +
    x_distributed_scan[i] * data["processing_times"]["distributed"]["scan"][i] * data["costs"]["distributed"]
    for i in range(N)
])

problem += total_cost

# Constraints
# Each cluster must have exactly one intervention type
for i in range(N):
    problem += (
        x_central_isolate[i] + x_central_scan[i] + x_distributed_isolate[i] + x_distributed_scan[i] == 1,
        f"One_Intervention_{i}"
    )

# Maximum hours for central processing
problem += (
    pulp.lpSum([
        x_central_isolate[i] * data["processing_times"]["central"]["isolate"][i] +
        x_central_scan[i] * data["processing_times"]["central"]["scan"][i]
        for i in range(N)
    ]) <= data["max_hours"]["central_max_hours"],
    "Max_Central_Hours"
)

# Maximum hours for distributed processing
problem += (
    pulp.lpSum([
        x_distributed_isolate[i] * data["processing_times"]["distributed"]["isolate"][i] +
        x_distributed_scan[i] * data["processing_times"]["distributed"]["scan"][i]
        for i in range(N)
    ]) <= data["max_hours"]["distributed_max_hours"],
    "Max_Distributed_Hours"
)

# Solve the problem
problem.solve()

# Output
interventions = []
for i in range(N):
    if pulp.value(x_central_isolate[i]) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "central", "amount": data["processing_times"]["central"]["isolate"][i]})
    elif pulp.value(x_central_scan[i]) == 1:
        interventions.append({"cluster_id": i, "type": "scan", "method": "central", "amount": data["processing_times"]["central"]["scan"][i]})
    elif pulp.value(x_distributed_isolate[i]) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "distributed", "amount": data["processing_times"]["distributed"]["isolate"][i]})
    elif pulp.value(x_distributed_scan[i]) == 1:
        interventions.append({"cluster_id": i, "type": "scan", "method": "distributed", "amount": data["processing_times"]["distributed"]["scan"][i]})

output = {
    "interventions": interventions,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')