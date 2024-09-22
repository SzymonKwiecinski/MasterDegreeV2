import pulp

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
setup_time = [12, 8, 4, 0]

P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Optimal_Batch_Production", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective Function
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * (
                   pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
                   (setup_time[p] * setup_flags[p] if m == 0 else 0)
               ) for m in range(M))

problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
        (pulp.lpSum(setup_time[p] * setup_flags[p] for p in range(P)) if m == 0 else 0)
        <= availability[m]), f"Machine_Availability_{m}"
    )

# Setup flag constraints
for p in range(P):
    problem += setup_flags[p] >= (batches[p] / M), f"Setup_Flag_Constraint_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')