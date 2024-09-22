import pulp

# Parse data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Define the number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the problem
problem = pulp.LpProblem("Auto Parts Manufacturer", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Define the objective function
profit = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
    pulp.lpSum(data['machine_costs'][m] * (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
        pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in range(P))
    ) for m in range(M))
)
problem += profit

# Add constraints
# Machine time availability constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
        pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in range(P)) <= data['availability'][m]
    )

# Solve the problem
problem.solve()

# Print the results
print("Batches produced:")
for p in range(P):
    print(f"Part {p+1}: {pulp.value(batches[p])}")

print("Setup flags:")
for p in range(P):
    print(f"Part {p+1}: {pulp.value(setup_flag[p])}")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")