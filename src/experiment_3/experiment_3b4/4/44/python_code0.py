import pulp

# Data from JSON
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

# Initialize problem
problem = pulp.LpProblem("MaximizeProfit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
total_profit = (
    pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - 
    pulp.lpSum([data['machine_costs'][m] * 
                pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) 
                for m in range(M)])
)

problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

# Minimum production constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')