import pulp

# Data from input
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Indices for parts and machines
P = len(prices)
M = len(machine_costs)

# Declare the LP problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
machine_hours_used = [pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum(machine_costs[m] * machine_hours_used[m] for m in range(1, M))
labor_cost = standard_cost * pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
overtime_labor_cost = overtime_cost * (machine_hours_used[0] - overtime_hour)
overtime_labor_cost = pulp.lpSum([overtime_labor_cost, 0]) # Only consider if there is overtime

total_cost = machine_cost + labor_cost + overtime_labor_cost
total_profit = profit - total_cost

problem += total_profit, "Total Profit"

# Constraints
for m in range(1, M):  # Machine hours constraints for m=2 to M
    problem += machine_hours_used[m] <= availability[m]

problem += total_profit >= min_profit

# Solve the problem
problem.solve()

# Prepare the results
result = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "total_profit": pulp.value(total_profit)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')