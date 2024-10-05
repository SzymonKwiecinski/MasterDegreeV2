import pulp

# Data from the provided JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Constants
num_parts = len(prices)
num_machines = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f"b_{p}", lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]

# Objective Function
profit_terms = [
    prices[p] * batches[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(num_machines))
    for p in range(num_parts)
]
problem += pulp.lpSum(profit_terms), "Total_Profit"

# Machine Availability Constraints
for m in range(num_machines):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m],
        f"Machine_{m}_Availability"
    )

# Solve the problem
problem.solve()

# Output the results
batches_solution = [pulp.value(b) for b in batches]
print("Optimal batch quantities:")
for p, batch_count in enumerate(batches_solution):
    print(f"Part {p + 1}: {batch_count:.2f} batches")

print(f'Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')