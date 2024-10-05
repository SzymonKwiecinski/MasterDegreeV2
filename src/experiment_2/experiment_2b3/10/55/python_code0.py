import pulp

# Load data
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

# Unpack data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Initialize model
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
hours_machine_1 = pulp.LpVariable('hours_machine_1', lowBound=0, cat='Continuous')
overtime_hours_machine_1 = pulp.LpVariable('overtime_hours_machine_1', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M))
labor_cost = standard_cost * hours_machine_1 + overtime_cost * overtime_hours_machine_1
profit = revenue - machine_cost - labor_cost
problem += profit

# Constraints
# Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine 1 time constraint considering overtime
total_hours_machine_1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += hours_machine_1 + overtime_hours_machine_1 == total_hours_machine_1
problem += hours_machine_1 <= overtime_hour

# Other machines' availability constraints
for m in range(1, M):
    machine_hours = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))
    problem += machine_hours <= availability[m]

# Profit constraint
problem += profit >= min_profit

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(profit)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')