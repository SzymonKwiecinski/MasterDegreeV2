import pulp

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Data
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]
machine_costs = [160, 10, 15]
availability = [200, 300, 500]
prices = [570, 250, 585, 430]
min_batches = [10, 10, 10, 10]

# Number of products and machines
P = len(prices)
M = len(machine_costs)

# Decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
revenue = pulp.lpSum([prices[p] * x[p] for p in range(P)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)])
objective = revenue - costs
problem += objective, "Total_Profit"

# Constraints
# Machine availability constraints for machines 0 to M-2
for m in range(M - 2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Combined availability constraint for machines M and M-1
problem += (pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) +
            pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P)) <= availability[M-1] + availability[M-2],
            "Combined_Availability_Constraint")

# Minimum batch requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Batch_Constraint_{p}"

# Solving the problem
problem.solve()

# Print the results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")