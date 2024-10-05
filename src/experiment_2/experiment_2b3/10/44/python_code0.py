import pulp

# Data inputs
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}

time_required = data["time_required"]
machine_costs = data["machine_costs"]
availability = data["availability"]
prices = data["prices"]
min_batches = data["min_batches"]

# Problem dimensions
num_machines = len(machine_costs)
num_parts = len(prices)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]

# Objective function: Maximize profit
profit = pulp.lpSum([(prices[p] * batches[p]) - pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for m in range(num_machines)]) for p in range(num_parts)])
problem += profit

# Constraints: Machine time availability
for m in range(num_machines):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m], f"Machine_{m}_availability"

# Solve the problem
problem.solve()

# Prepare the output
batches_produced = [pulp.value(batches[p]) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')