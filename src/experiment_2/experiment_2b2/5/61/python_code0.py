import pulp

# Define data from JSON
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

# Extract data
N = len(data["processing_times"]["central"]["isolate"])
central_cost = data["costs"]["central"]
distributed_cost = data["costs"]["distributed"]
max_central = data["max_hours"]["central_max_hours"]
max_distributed = data["max_hours"]["distributed_max_hours"]

proc_times = data["processing_times"]

# Initialize problem
problem = pulp.LpProblem("Network_Intervention_Problem", pulp.LpMinimize)

# Define decision variables
vars = {
    "central_isolate": [pulp.LpVariable(f"central_isolate_{i}", cat='Binary') for i in range(N)],
    "central_scan": [pulp.LpVariable(f"central_scan_{i}", cat='Binary') for i in range(N)],
    "distributed_isolate": [pulp.LpVariable(f"distributed_isolate_{i}", cat='Binary') for i in range(N)],
    "distributed_scan": [pulp.LpVariable(f"distributed_scan_{i}", cat='Binary') for i in range(N)]
}

# Objective function
problem += pulp.lpSum(
    central_cost * (proc_times["central"]["isolate"][i] * vars["central_isolate"][i] +
    proc_times["central"]["scan"][i] * vars["central_scan"][i]) +
    distributed_cost * (proc_times["distributed"]["isolate"][i] * vars["distributed_isolate"][i] +
    proc_times["distributed"]["scan"][i] * vars["distributed_scan"][i])
    for i in range(N)
)

# Constraints
for i in range(N):
    # Each cluster must have one intervention type and processing method
    problem += vars["central_isolate"][i] + vars["central_scan"][i] + \
               vars["distributed_isolate"][i] + vars["distributed_scan"][i] == 1

# Which cannot exceed the respective maximum hours
problem += pulp.lpSum(
    proc_times["central"]["isolate"][i] * vars["central_isolate"][i] +
    proc_times["central"]["scan"][i] * vars["central_scan"][i]
    for i in range(N)
) <= max_central

problem += pulp.lpSum(
    proc_times["distributed"]["isolate"][i] * vars["distributed_isolate"][i] +
    proc_times["distributed"]["scan"][i] * vars["distributed_scan"][i]
    for i in range(N)
) <= max_distributed

# Solve the problem
problem.solve()

# Generate output
interventions = []
for i in range(N):
    if pulp.value(vars["central_isolate"][i]) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "central",
                              "amount": proc_times["central"]["isolate"][i]})
    elif pulp.value(vars["central_scan"][i]) == 1:
        interventions.append({"cluster_id": i, "type": "scan", "method": "central",
                              "amount": proc_times["central"]["scan"][i]})
    elif pulp.value(vars["distributed_isolate"][i]) == 1:
        interventions.append({"cluster_id": i, "type": "isolate", "method": "distributed",
                              "amount": proc_times["distributed"]["isolate"][i]})
    elif pulp.value(vars["distributed_scan"][i]) == 1:
        interventions.append({"cluster_id": i, "type": "scan", "method": "distributed",
                              "amount": proc_times["distributed"]["scan"][i]})

total_cost = pulp.value(problem.objective)

# Assemble and print final output
output = {
    "interventions": interventions,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')