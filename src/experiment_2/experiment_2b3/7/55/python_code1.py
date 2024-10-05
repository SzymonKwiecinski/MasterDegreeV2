import pulp

# Parsing the data
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

P = len(prices)
M = len(machine_costs)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of batches to produce for each part
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Additional decision variable for machine 1's labor hours
labor_hours = pulp.LpVariable('labor_hours', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)]) \
         - pulp.lpSum([batches[p] * time_required[0][p] for p in range(P)]) * standard_cost \
         - (overtime_cost - standard_cost) * pulp.lpMax(0, labor_hours - overtime_hour) \
         - pulp.lpSum([machine_costs[m] * pulp.lpSum([batches[p] * time_required[m][p] for p in range(P)]) for m in range(1, M)])

# Set the objective
problem += profit, "Total Profit"

# Constraints

# Machine availabilities (excluding machine 1)
for m in range(1, M):
    problem += pulp.lpSum([batches[p] * time_required[m][p] for p in range(P)]) <= availability[m], f"Machine_{m}_availability"

# Machine 1 labor hours
total_hours_machine_1 = pulp.lpSum([batches[p] * time_required[0][p] for p in range(P)])
problem += (labor_hours == total_hours_machine_1), "Labor_Hours_Machine_1"

# Ensure minimum profit
problem += profit >= min_profit, "Minimum_Profit"

# Solve the problem
problem.solve()

# Output the results
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')