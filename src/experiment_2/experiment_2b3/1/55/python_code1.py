import pulp

# Data input
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

# Extract details
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]
machine_1_hours = pulp.LpVariable('machine_1_hours', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_costs_expression = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(1, M)])
machine_1_cost = pulp.lpSum([(standard_cost * pulp.lpMin(machine_1_hours, overtime_hour)) +
                               (overtime_cost * pulp.lpMax(0, machine_1_hours - overtime_hour))])

profit = revenue - (machine_costs_expression + machine_1_cost)
problem += profit, "Total_Profit"

# Constraints

# Machine 1 cost and hours
problem += machine_1_hours == pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])

# Availability constraints (only for Machines 2 to M)
for m in range(1, M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Minimum profit condition
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')