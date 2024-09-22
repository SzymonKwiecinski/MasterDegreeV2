import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Sets and indices
P = range(len(data['prices']))  # Parts
M = range(len(data['machine_costs']))  # Machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", P, cat='Binary')

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) for m in M) - \
         pulp.lpSum(data['setup_time'][p] * setup_flag[p] * data['machine_costs'][0] for p in P)

problem += profit

# Constraints
for m in M:
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) +
                 (1 if m == 0 else 0) * pulp.lpSum(data['setup_time'][p] * setup_flag[p] for p in P) 
                 <= data['availability'][m], f"Availability_Constraint_Machine_{m}")

for p in P:
    problem += setup_flag[p] <= batches[p], f"Setup_Constraint_Part_{p}"

# Solve the optimization problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')