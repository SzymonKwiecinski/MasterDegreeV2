import pulp

# Data from the JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Problem Definition
problem = pulp.LpProblem("Auto Parts Production", pulp.LpMaximize)

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective Function
total_profit = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
    - pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
    - pulp.lpSum(data['setup_time'][p] * setup_flags[p] * data['machine_costs'][0] for p in range(P))
)

problem += total_profit

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
        + (data['setup_time'][p] * setup_flags[p] if m == 0 else 0)
        <= data['availability'][m]
    )

# Setup Flag Constraints
for p in range(P):
    problem += batches[p] <= M * setup_flags[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')