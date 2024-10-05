import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Indices
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Create problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective Function
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * 
                           (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) +
                            pulp.lpSum([setup_flags[p] * data['setup_time'][p] for p in range(P)] if m == 0 else 0))
                           for m in range(M)])

problem += total_profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) +
                (pulp.lpSum([setup_flags[p] * data['setup_time'][p] for p in range(P)]) if m == 0 else 0)
               <= data['availability'][m])

# Solve the problem
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output batches and setup flags for each part
batches_output = [pulp.value(batches[p]) for p in range(P)]
setup_flags_output = [pulp.value(setup_flags[p]) for p in range(P)]

# Output results
print("Batches produced for each part:", batches_output)
print("Setup flags for each part:", setup_flags_output)