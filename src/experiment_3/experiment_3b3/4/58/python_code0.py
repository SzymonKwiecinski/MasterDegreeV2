import pulp

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
setup_time = [12, 8, 4, 0]

P = range(len(prices))  # Number of parts
M = range(len(machine_costs))  # Number of machines

# Problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in P]
setup_flag = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in P]

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in P)
cost = pulp.lpSum(
    machine_costs[m] * (sum(time_required[m][p] * batches[p] for p in P) +
                        sum(setup_flag[p] * setup_time[p] for p in P if m == 0))
    for m in M
)
problem += profit - cost

# Constraints
for m in M:
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in P) + \
               pulp.lpSum(setup_flag[p] * setup_time[p] for p in P if m == 0) <= availability[m]

# Solve
problem.solve()

# Output
for p in P:
    print(f'Batches produced for part {p+1}: {batches[p].varValue}')
    print(f'Setup flag for part {p+1}: {setup_flag[p].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')