import pulp

# Data from JSON input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

# Extracting data
time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
setup_time = data["setup_time"]

# Problem data
M = len(machine_costs)  # number of machines
P = len(prices)  # number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum([
    prices[p] * batches[p] - sum((time_required[m][p] * batches[p] + (setup_time[p] * setup_flags[p] if m == 0 else 0)) * machine_costs[m] 
    for m in range(M)) 
    for p in range(P)
])

problem += profit

# Constraints
for m in range(M):
    machine_hours = pulp.lpSum([
        time_required[m][p] * batches[p] + (setup_time[p] * setup_flags[p] if m == 0 else 0) 
        for p in range(P)
    ])
    problem += machine_hours <= availability[m], f"Machine_{m}_Availability"

# Solve the problem
problem.solve()

# Get the results
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output in the specified format
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')