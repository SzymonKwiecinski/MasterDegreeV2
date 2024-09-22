import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Indices
P = len(data['prices'])      # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Objective Function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - pulp.lpSum(
    (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
     (1 if m == 0 else 0) * pulp.lpSum(setup_flags[p] * data['setup_time'][p] for p in range(P))
    ) * data['machine_costs'][m] 
    for m in range(M)
)

problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
        (1 if m == 0 else 0) * pulp.lpSum(setup_flags[p] * data['setup_time'][p] for p in range(P))
        <= data['availability'][m]
    )

# Setup flags constraints
for p in range(P):
    problem += setup_flags[p] >= (batches[p] / M)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')