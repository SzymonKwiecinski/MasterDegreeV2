import pulp

# Data from the problem
data = {
    "processing_times": {
        "central": {"isolate": [10, 6, 8], "scan": [6, 4, 6]},
        "distributed": {"isolate": [12, 9, 12], "scan": [18, 10, 15]}
    },
    "costs": {"central": 150, "distributed": 70},
    "max_hours": {"central_max_hours": 16, "distributed_max_hours": 33}
}

central_cost = data["costs"]["central"]
distributed_cost = data["costs"]["distributed"]

isolate_central = data["processing_times"]["central"]["isolate"]
scan_central = data["processing_times"]["central"]["scan"]
isolate_distributed = data["processing_times"]["distributed"]["isolate"]
scan_distributed = data["processing_times"]["distributed"]["scan"]

max_central = data["max_hours"]["central_max_hours"]
max_distributed = data["max_hours"]["distributed_max_hours"]

N = len(isolate_central)

# Define the problem
problem = pulp.LpProblem("NetworkIntrusionIntervention", pulp.LpMinimize)

# Decision Variables
x_c_isolate = [pulp.LpVariable(f"x_c_isolate_{i}", cat='Binary') for i in range(N)]
x_c_scan = [pulp.LpVariable(f"x_c_scan_{i}", cat='Binary') for i in range(N)]
x_d_isolate = [pulp.LpVariable(f"x_d_isolate_{i}", cat='Binary') for i in range(N)]
x_d_scan = [pulp.LpVariable(f"x_d_scan_{i}", cat='Binary') for i in range(N)]
t = [pulp.LpVariable(f"t_{i}", lowBound=0) for i in range(N)]

# Objective Function
problem += (
    pulp.lpSum(central_cost * (x_c_isolate[i] * isolate_central[i] + x_c_scan[i] * scan_central[i]) for i in range(N)) +
    pulp.lpSum(distributed_cost * (x_d_isolate[i] * isolate_distributed[i] + x_d_scan[i] * scan_distributed[i]) for i in range(N))
)

# Constraints
for i in range(N):
    # Each cluster must be assigned exactly one intervention method
    problem += (x_c_isolate[i] + x_c_scan[i] + x_d_isolate[i] + x_d_scan[i] == 1)

# Total central processing time must not exceed the maximum allowed
problem += (
    pulp.lpSum(x_c_isolate[i] * t[i] + x_c_scan[i] * t[i] for i in range(N)) <= max_central
)

# Total distributed processing time must not exceed the maximum allowed
problem += (
    pulp.lpSum(x_d_isolate[i] * t[i] + x_d_scan[i] * t[i] for i in range(N)) <= max_distributed
)

# Linking decision variables to processing times
for i in range(N):
    problem += (t[i] >= x_c_isolate[i] * isolate_central[i])
    problem += (t[i] >= x_c_scan[i] * scan_central[i])
    problem += (t[i] >= x_d_isolate[i] * isolate_distributed[i])
    problem += (t[i] >= x_d_scan[i] * scan_distributed[i])

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')