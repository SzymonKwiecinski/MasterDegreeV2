import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])    # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
batches_vars = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
revenue = pulp.lpSum(data['prices'][p] * batches_vars[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches_vars[p] for p in range(P)) for m in range(M))
problem += revenue - cost

# Constraints

# Minimum Production Requirement
for p in range(P):
    problem += batches_vars[p] >= data['min_batches'][p]

# Machine Availability Constraints for 1 to M-2
for m in range(M-2):
    problem += pulp.lpSum(data['time_required'][m][p] * batches_vars[p] for p in range(P)) <= data['availability'][m]

# Combined machine availability for M-1 and M
problem += (pulp.lpSum(data['time_required'][M-1][p] * batches_vars[p] for p in range(P)) + 
            pulp.lpSum(data['time_required'][M-2][p] * batches_vars[p] for p in range(P)) <= 
            data['availability'][M-1] + data['availability'][M-2])

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')