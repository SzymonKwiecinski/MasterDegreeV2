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

# Unpacking the input data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

M = len(time_required)   # Number of machines
P = len(prices)          # Number of parts

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches of each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Additional variables for overtime on machine 1
standard_hours = pulp.LpVariable('standard_hours', lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
machine_costs_total = pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for m in range(M) for p in range(P)])
labor_cost = (standard_hours * standard_cost) + (overtime_hours * overtime_cost)

profit = revenue - (machine_costs_total + labor_cost)
problem += profit

# Constraints
# Machine time constraints
for m in range(1, M):  # Starting from machine 2 since machine 1 is outsourced
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Labor time for machine 1
problem += standard_hours + overtime_hours == pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
problem += standard_hours <= overtime_hour  # Standard hours constraint

# Minimum profit constraint
problem += profit >= min_profit

# Solve the problem
status = problem.solve()

# Output the results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit)

print({
    "batches": batches_result,
    "total_profit": total_profit
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')