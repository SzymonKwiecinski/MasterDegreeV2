import pulp

# Data provided in the problem
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

# Extract values from the data dictionary
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

# Create a linear programming problem
problem = pulp.LpProblem("Produce_Auto_Parts", pulp.LpMaximize)

# Decision variables for number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Decision variables for overtime hours on machine 1
overtime_hours_machine_1 = pulp.LpVariable('overtime_hours_machine_1', lowBound=0, cat='Continuous')

# Total profit calculation
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M)
)

# Machine 1 cost calculation with standard and overtime
machine_1_hours = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
standard_hours_cost = standard_cost * pulp.lpSum(machine_1_hours)
overtime_cost_component = overtime_cost * (machine_1_hours - overtime_hour)
machine_1_total_cost = pulp.LpVariable('machine_1_total_cost', lowBound=0, cat='Continuous')
problem += (machine_1_total_cost == standard_hours_cost + overtime_cost_component * 
           (machine_1_hours > overtime_hour))

# Profit definition
profit = total_revenue - (total_cost + machine_1_total_cost)

# Set the objective function: maximize profit
problem += profit, "Total Profit"

# Constraints
# Machine capacity constraints (excluding Machine 1)
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum profit constraint
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Prepare the output in the specified format
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')