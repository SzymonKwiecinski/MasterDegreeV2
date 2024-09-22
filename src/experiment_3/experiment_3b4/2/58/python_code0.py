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
num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(num_parts), cat='Binary')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(
    data['prices'][p] * batches[p] for p in range(num_parts)
) - pulp.lpSum(
    data['time_required'][m][p] * batches[p] * data['machine_costs'][m] for m in range(num_machines) for p in range(num_parts)
) - pulp.lpSum(
    setup_flags[p] * data['setup_time'][p] * data['machine_costs'][0] for p in range(num_parts)
)

problem += profit

# Constraints
# Machine Time Constraints
for m in range(num_machines):
    if m == 0:
        problem += pulp.lpSum(
            data['time_required'][m][p] * batches[p] for p in range(num_parts)
        ) + pulp.lpSum(
            setup_flags[p] * data['setup_time'][p] for p in range(num_parts)
        ) <= data['availability'][m]
    else:
        problem += pulp.lpSum(
            data['time_required'][m][p] * batches[p] for p in range(num_parts)
        ) <= data['availability'][m]

# Setup Constraint for Machine 1
for p in range(num_parts):
    problem += setup_flags[p] >= batches[p] / (1 + batches[p])

# Solve the Problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')