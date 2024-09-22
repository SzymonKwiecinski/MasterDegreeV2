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

# Constants from data
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

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit_expression = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
cost_expression = pulp.lpSum([
    machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])
    for m in range(M)
])

# Labor Cost Calculation for Machine 1
H = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
labor_cost = pulp.LpVariable('labor_cost', lowBound=0, cat='Continuous')

problem += labor_cost == (
    pulp.lpSum([
        (time_required[0][p] * batches[p] * standard_cost) for p in range(P)
    ]) * (H <= overtime_hour) + 
    ((standard_cost * overtime_hour + overtime_cost * (H - overtime_hour)) * (H > overtime_hour))
)

# Total profit
total_profit = profit_expression - cost_expression - labor_cost
problem += total_profit, "Total_Profit"

# Constraints
# Machine Availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_{m}_Availability"

# Minimum Profit
problem += total_profit >= min_profit, "Min_Profit"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    print(f'Number of batches for part {p+1}: {batches[p].varValue}')

print(f'Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')