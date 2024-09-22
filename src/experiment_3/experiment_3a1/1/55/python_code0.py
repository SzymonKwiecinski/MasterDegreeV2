import pulp

# Data from the provided JSON
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

# Extracting parameters from data
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

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([(prices[p] * b[p]) for p in range(P)])  # Revenue
labor_cost = standard_cost * (overtime_hour * (pulp.lpSum([time_required[m][p] * b[p] for p in range(P) for m in range(M)]) - overtime_hour))
overtime_cost_total = pulp.lpSum([overtime_cost * (pulp.lpSum([time_required[m][p] * b[p] for p in range(P)]) - overtime_hour) for m in range(M)])
total_cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * b[p] for p in range(P)]) for m in range(M)]) + labor_cost + overtime_cost_total
problem += profit - total_cost, "Total Profit"

# Constraints
# Machine Availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * b[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Minimum Batch Requirement
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Batches_{p}"

# Desired Profit
problem += profit - total_cost >= min_profit, "Min_Profit"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Number of batches produced for part {p+1}: {b[p].varValue}')

# Total Profit
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')