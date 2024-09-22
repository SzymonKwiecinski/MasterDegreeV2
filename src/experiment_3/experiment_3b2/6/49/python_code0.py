import pulp

# Data extracted from the provided JSON
time_required = [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]]  # time required for each machine and part
machine_costs = [160, 10, 15]  # costs per hour for each machine
availability = [200, 300, 500]  # available hours for each machine
prices = [570, 250, 585, 430]  # selling prices for each part
min_batches = [10, 10, 10, 10]  # minimum batches for each part

# Set up the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
parts = range(len(prices))  # parts indexed by p
batches = pulp.LpVariable.dicts("batches", parts, lowBound=0)  # batches of parts to produce

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in parts)
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in parts) for m in range(len(machine_costs)))
problem += revenue - cost, "Total_Profit"

# Constraints
# Machine time availability constraints for machines 1 to M-2
for m in range(len(machine_costs) - 2):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in parts) <= availability[m], f"Machine_{m+1}_availability"

# Combined availability constraint for machines M and M-1
problem += pulp.lpSum((time_required[-2][p] + time_required[-1][p]) * batches[p] for p in parts) <= availability[-2] + availability[-1], "Combined_availability"

# Minimum production requirements
for p in parts:
    problem += batches[p] >= min_batches[p], f"Min_batches_for_part_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')