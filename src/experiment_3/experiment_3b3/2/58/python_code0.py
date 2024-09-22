import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Calculation of P and M
P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Production_Problem", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(
    machine_costs[m] * (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P))
    ) for m in range(M)
)
problem += profit - costs, "Total Profit"

# Constraints
for m in range(M):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P))
        <= availability[m]
    ), f"Machine_Avail_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')