import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]

# Objective function
# Maximize: sum(Prices_p * x_p) - sum(MachineCosts_m * sum(TimeRequired_m,p * x_p))
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P))
costs = pulp.lpSum(data['machine_costs'][m] * 
                   pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P))
                   for m in range(M))

problem += profit - costs

# Constraints

# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')