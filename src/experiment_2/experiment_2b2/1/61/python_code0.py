import pulp

# Input data
data = {'processing_times': {'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]}, 'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}}, 'costs': {'central': 150, 'distributed': 70}, 'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}}

# Extract data
processing_times = data["processing_times"]
central_cost = data["costs"]["central"]
distributed_cost = data["costs"]["distributed"]
max_central = data["max_hours"]["central_max_hours"]
max_distributed = data["max_hours"]["distributed_max_hours"]

# Number of clusters
N = len(processing_times["central"]["isolate"])

# Define the MILP problem
problem = pulp.LpProblem("Intrusion_Intervention", pulp.LpMinimize)

# Decision variables
# 1 if intervention is 'isolate' for cluster i using 'central', else 0
central_isolate_vars = [
    pulp.LpVariable(f"central_isolate_{i}", cat="Binary") for i in range(N)
]
# 1 if intervention is 'scan' for cluster i using 'central', else 0
central_scan_vars = [
    pulp.LpVariable(f"central_scan_{i}", cat="Binary") for i in range(N)
]
# 1 if intervention is 'isolate' for cluster i using 'distributed', else 0
distributed_isolate_vars = [
    pulp.LpVariable(f"distributed_isolate_{i}", cat="Binary") for i in range(N)
]
# 1 if intervention is 'scan' for cluster i using 'distributed', else 0
distributed_scan_vars = [
    pulp.LpVariable(f"distributed_scan_{i}", cat="Binary") for i in range(N)
]

# Objective function: Minimize the total cost
problem += pulp.lpSum(
    [
        (central_cost / 1) * (central_isolate_vars[i] * processing_times["central"]["isolate"][i] + central_scan_vars[i] * processing_times["central"]["scan"][i])
        + (distributed_cost / 1) * (distributed_isolate_vars[i] * processing_times["distributed"]["isolate"][i] + distributed_scan_vars[i] * processing_times["distributed"]["scan"][i])
        for i in range(N)
    ]
)

# Constraints:
# Each cluster needs one type of intervention (either 'isolate' or 'scan') and one method (either 'central' or 'distributed')
for i in range(N):
    problem += (
        central_isolate_vars[i]
        + central_scan_vars[i]
        + distributed_isolate_vars[i]
        + distributed_scan_vars[i]
        == 1
    )

# Maximum central processing hours constraint
problem += pulp.lpSum(
    [
        central_isolate_vars[i] * processing_times["central"]["isolate"][i]
        + central_scan_vars[i] * processing_times["central"]["scan"][i]
        for i in range(N)
    ]
) <= max_central

# Maximum distributed processing hours constraint
problem += pulp.lpSum(
    [
        distributed_isolate_vars[i] * processing_times["distributed"]["isolate"][i]
        + distributed_scan_vars[i] * processing_times["distributed"]["scan"][i]
        for i in range(N)
    ]
) <= max_distributed

# Solve the problem
problem.solve()

# Prepare the output
interventions = []
for i in range(N):
    if pulp.value(central_isolate_vars[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "central", "amount": processing_times["central"]["isolate"][i]})
    elif pulp.value(central_scan_vars[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "central", "amount": processing_times["central"]["scan"][i]})
    elif pulp.value(distributed_isolate_vars[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "isolate", "method": "distributed", "amount": processing_times["distributed"]["isolate"][i]})
    elif pulp.value(distributed_scan_vars[i]) == 1:
        interventions.append({"cluster_id": i+1, "type": "scan", "method": "distributed", "amount": processing_times["distributed"]["scan"][i]})

total_cost = pulp.value(problem.objective)

output = {"interventions": interventions, "total_cost": total_cost}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')