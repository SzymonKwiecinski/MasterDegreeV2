import pulp

# Data from JSON
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

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

num_parts = len(prices)
num_machines = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(num_parts)]

# Expression for profit calculation
total_revenue = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)])

# Machine Time Constraints
machine_time_constraints = [
    pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m]
    for m in range(num_machines)
]

# Minimum Batch Production
min_batch_constraints = [batches[p] >= min_batches[p] for p in range(num_parts)]

# Total Hours on Machine 1
T = pulp.lpSum([time_required[0][p] * batches[p] for p in range(num_parts)])

# Labor Cost Calculation for Machine 1
labor_cost = pulp.LpVariable('labor_cost', lowBound=0, cat='Continuous')
overtime_hours = T - overtime_hour

problem += labor_cost == (
    standard_cost * T + (overtime_cost - standard_cost) * overtime_hours * (overtime_hours > 0)
)

# Total Cost
total_machine_cost = pulp.lpSum([
    machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) 
    for m in range(num_machines)
])

total_cost = total_machine_cost + labor_cost

# Objective Function
profit = total_revenue - total_cost
problem += profit

# Profit Constraint
problem += profit >= min_profit

# Add constraints to the problem
for cons in machine_time_constraints + min_batch_constraints:
    problem += cons

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')