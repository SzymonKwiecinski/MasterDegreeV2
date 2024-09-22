import pulp

# Data input from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the LP problem
problem = pulp.LpProblem("Batch_Production_Problem", pulp.LpMaximize)

# Decision variables: number of batches to produce for each part
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: maximize profit
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_machine_costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
machine_1_usage = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))

# Standard and overtime costs for machine 1
standard_costs = pulp.lpSum(standard_cost * machine_1_usage)
overtime_costs = overtime_cost * (machine_1_usage - overtime_hour)
total_costs = total_machine_costs + standard_costs + pulp.lpSum(pulp.lpMax(0, overtime_costs))

# Profit = Revenue - Costs
profit = total_revenue - total_costs

# Add the objective
problem += profit, "Total_Profit"

# Constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m}_Availability"

# Minimum profit constraint
problem += profit >= min_profit, "Minimum_Profit"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [pulp.value(batch) for batch in batches],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')