import pulp

# Data from JSON
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

# Constants
M = data['NumMachines']
P = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of batches of each part p
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Extra variables for Machine 1 due to labor cost: standard hours and overtime hours
standard_hours = pulp.LpVariable('standard_hours', lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0, cat='Continuous')

# Objective function: Maximize profit
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(1, M)
)
labor_cost = standard_cost * standard_hours + overtime_cost * overtime_hours

# Set the objective
problem += revenue - machine_cost - labor_cost

# Constraints

# Standard and Overtime hours for Machine 1
total_hours_machine_1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
problem += (standard_hours + overtime_hours == total_hours_machine_1)
problem += (standard_hours <= overtime_hour[0])
problem += (overtime_hours >= 0)

# Machine availability constraints except Machine 1
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Collect results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')