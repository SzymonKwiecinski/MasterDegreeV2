import pulp

# Load data
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

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define LP problem
problem = pulp.LpProblem("Parts_Production_Optimization", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]
hours_on_machine_1 = pulp.LpVariable("hours_on_machine_1", lowBound=0, cat='Continuous')
overtime_hours_machine_1 = pulp.LpVariable("overtime_hours_machine_1", lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
production_costs = pulp.lpSum([time_required[m][p] * machine_costs[m] * batches[p] for p in range(P) for m in range(1, M)])
machine_1_costs = hours_on_machine_1 * standard_cost + overtime_hours_machine_1 * (overtime_cost - standard_cost)
total_costs = production_costs + machine_1_costs
profit = revenue - total_costs
problem += profit, "Total Profit"

# Constraints
# Total hours on machine 1
problem += hours_on_machine_1 == pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]), "Machine_1_Hour_Calculation"
# Overtime hours on machine 1
problem += overtime_hours_machine_1 >= hours_on_machine_1 - overtime_hour, "Overtime_Hours_Machine_1"
# Machine availability constraints (except Machine 1, which is outsourced)
for m in range(1, M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Machine_{m+1}"

# Minimum profit constraint
problem += profit >= min_profit, "Minimum_Profit_Constraint"

# Solve the problem
problem.solve()

# Output
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit)
result = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')