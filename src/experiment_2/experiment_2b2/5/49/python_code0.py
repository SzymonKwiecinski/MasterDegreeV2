import pulp

# Extract the data from the provided JSON data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define the number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables for the number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective function: Maximize the profit
# Profit = Revenue - Cost
revenue = pulp.lpSum(batches[p] * data['prices'][p] for p in range(P))
cost = pulp.lpSum(batches[p] * data['time_required'][m][p] * data['machine_costs'][m] for m in range(M) for p in range(P))
problem += revenue - cost

# Constraints
# Machine time availability constraints
availability_constraints = [[batches[p] * data['time_required'][m][p] for p in range(P)] for m in range(M)]

for m in range(M - 2):  # For machines 1 to M-2
    problem += pulp.lpSum(availability_constraints[m]) <= data['availability'][m]

# Combine availability for Machine M and Machine M-1
problem += pulp.lpSum(availability_constraints[M-1]) + pulp.lpSum(availability_constraints[M-2]) <= data['availability'][M-1] + data['availability'][M-2]

# Solve the problem
problem.solve()

# Prepare the output results
batches_result = [pulp.value(batch) for batch in batches]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')