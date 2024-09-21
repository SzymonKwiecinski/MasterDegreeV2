import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M))
problem += profit - costs

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m], f"Machine_Availability_{m}"

# Solve the problem
problem.solve()

# Print the optimized objective function value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')