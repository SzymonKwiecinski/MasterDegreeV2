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

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Number of parts and machines
num_parts = len(prices)
num_machines = len(machine_costs)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]

# Objective function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)])
costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) for m in range(1, num_machines)])
machine_1_hours = pulp.lpSum([time_required[0][p] * batches[p] for p in range(num_parts)])

# Standard and Overtime cost calculation for Machine 1
standard_cost_calc = standard_cost * pulp.lpSum([time_required[0][p] * batches[p] for p in range(num_parts)])
overtime_cost_calc = overtime_cost * (machine_1_hours - overtime_hour)

# Ensure overtime cost only applies when hours exceed overtime_hour
overtime_cost_calc_final = pulp.LpVariable('overtime_cost_calc', lowBound=0, cat='Continuous')
problem += overtime_cost_calc_final >= overtime_cost_calc

# Total cost
total_cost = costs + standard_cost_calc + overtime_cost_calc_final

# Add objective
problem += profit - total_cost

# Constraints
# Machine availability constraints for machines 2 to M
for m in range(1, num_machines):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m]
    
# Minimum profit constraint
problem += profit - total_cost >= min_profit

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(num_parts)],
    "total_profit": pulp.value(profit - total_cost)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')