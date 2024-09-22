import pulp

# Input data
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

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Dimensions
P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(P)]

# Overtime hours for machine 1
overtime_hours_m1 = pulp.LpVariable('overtime_hours_m1', 0, None, cat='Continuous')

# Add profit objective
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
standard_hours_m1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
cost_machines = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
labor_cost = standard_cost * (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) - overtime_hours_m1) + overtime_cost * overtime_hours_m1

profit = revenue - (labor_cost + cost_machines)
problem += profit, "Total_Profit"

# Constraints
# Machine 1 constraints (consider labor cost)
problem += overtime_hours_m1 >= 0
problem += standard_hours_m1 <= overtime_hours_m1 + overtime_hour

# Machine 2 and onwards constraints
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum profit constraint
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Collect results
result_batches = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit)

# Output
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')