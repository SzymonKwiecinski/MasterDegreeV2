import pulp

# Define the data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Set the number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define the decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Define the objective function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P))
machine_cost = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P))
    for m in range(M)
)
problem += profit - machine_cost, "Total Profit"

# Define the constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

# Minimum batches constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Batches_Part_{p}"

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    print(f"Number of batches for part {p+1}: {pulp.value(x[p])}")

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")