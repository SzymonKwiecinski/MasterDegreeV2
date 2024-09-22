import pulp

# Data extraction from the provided JSON data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Define sets
P = range(len(data['prices']))  # Number of parts
M = range(len(data['machine_costs']))  # Number of machines

# Create the problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Continuous')
setup_flags = pulp.LpVariable.dicts("setup_flags", P, cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) + 
                      pulp.lpSum(data['setup_time'][p] * setup_flags[p] for p in P)) 
                     for m in M)

problem += profit, "Total Profit"

# Constraints
for m in M:
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) +
                 pulp.lpSum(data['setup_time'][p] * setup_flags[p] for p in P) <= 
                 data['availability'][m]), f"Machine_{m}_Availability"

# Solve the problem
problem.solve()

# Output results
for p in P:
    print(f'Batches of part {p}: {batches[p].varValue}')
    print(f'Setup for part {p}: {setup_flags[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')