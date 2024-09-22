import pulp

# Data from JSON input
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "setup_time": [12, 8, 4, 0]
}

# Unpack data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

M = len(time_required)
P = len(time_required[0])

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for number of batches
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]

# Decision variables for setup flags (binary)
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] - setup_flags[p] * setup_time[p] * machine_costs[0] for p in range(P)])
usage_cost = pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for m in range(M) for p in range(P)])
problem += profit - usage_cost, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], 
                f"Machine_{m}_Availability")

# Setup time constraints for machine 1 (m=0)
for p in range(P):
    problem += (batches[p] * setup_time[p] <= setup_flags[p] * availability[0], 
                f"Setup_Time_Constraint_{p}")

# Solve the problem
problem.solve()

# Collect the results
batches_result = [int(batches[p].varValue) for p in range(P)]
setup_flags_result = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print output
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')