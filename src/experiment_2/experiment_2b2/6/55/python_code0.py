import pulp

# Data from JSON input
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

# Unpacking data
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

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
hours_on_machine_1 = pulp.LpVariable("hours_on_machine_1", lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable("overtime_hours", lowBound=0, cat='Continuous')

# Objective function: Maximize profit
total_revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
operating_costs = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(1, M)])
machine_1_cost = standard_cost * hours_on_machine_1 + overtime_cost * overtime_hours
total_profit = total_revenue - operating_costs - machine_1_cost

# Set the objective
problem += total_profit

# Constraints for machine availability
for m in range(1, M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Machine_{m+1}"

# Constraint for machine 1 (outsourced)
problem += hours_on_machine_1 == pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
problem += hours_on_machine_1 <= overtime_hour + overtime_hours

# Constraint for minimum profit
problem += total_profit >= min_profit, "Minimum_Profit"

# Solve the problem
problem.solve()

# Extracting the solution
batches_solution = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(total_profit)

# Prepare the output in the specified format
output = {
    "batches": batches_solution,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')