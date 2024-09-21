import pulp

# Data provided
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(M)])
problem += profit - costs

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m]

# Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Print out the result
for p in range(P):
    print(f"Number of batches for part {p + 1}: {x[p].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')