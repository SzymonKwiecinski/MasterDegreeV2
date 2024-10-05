import pulp

# Extracted data from JSON format
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - costs, "Total Profit"

# Constraints

# Machine availability constraint
problem += pulp.lpSum([pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)]) <= pulp.lpSum(availability), "Availability Constraint"

# Minimum production requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum Batches for Part {p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')