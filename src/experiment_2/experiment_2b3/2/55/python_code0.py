import pulp

# Data
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

# Define LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Decision variables: batches to produce for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Auxiliary variable for Machine 1 - outsourcing
hours_on_machine_1 = sum(time_required[0][p] * batches[p] for p in range(P))
regular_hours = pulp.LpVariable('regular_hours', lowBound=0, upBound=overtime_hour, cat='Continuous')
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0, cat='Continuous')

# Constraints
# Machine usage constraints
for m in range(1, M):
    machine_usage = sum(time_required[m][p] * batches[p] for p in range(P))
    problem += machine_usage <= availability[m], f'Availability_constraint_machine_{m+1}'

# Machine 1 (outsourced)
problem += regular_hours + overtime_hours == hours_on_machine_1, "Machine_1_hours_balance"

# Profit calculation
sales_revenue = sum(prices[p] * batches[p] for p in range(P))
machine_cost_total = sum(machine_costs[m] * sum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
labor_cost = standard_cost * regular_hours + overtime_cost * overtime_hours
total_costs = machine_cost_total + labor_cost
profit = sales_revenue - total_costs

# Objective function
problem += profit

# Minimum profit constraint
problem += profit >= min_profit, "Minimum_profit"

# Solve the problem
problem.solve()

# Collect results
batches_result = [pulp.value(batches[p]) for p in range(P)]
objective_value = pulp.value(problem.objective)

# Output Results
output = {
    "batches": batches_result,
    "total_profit": objective_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')