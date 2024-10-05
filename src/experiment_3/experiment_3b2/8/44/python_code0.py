import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
num_parts = len(data['prices'])
x = pulp.LpVariable.dicts('Batch', range(num_parts), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(num_parts))
costs = pulp.lpSum(data['machine_costs'][m] * data['time_required'][m][p] * x[p]
                   for m in range(len(data['machine_costs'])) for p in range(num_parts))
problem += profit - costs

# Constraints
# Machine Availability Constraints
for m in range(len(data['availability'])):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) <= data['availability'][m])

# Minimum Batch Requirement Constraints
for p in range(num_parts):
    problem += (x[p] >= data['min_batches'][p])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')