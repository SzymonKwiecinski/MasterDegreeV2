import pulp

# Parse input data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(P)]
x1_regular = pulp.LpVariable(f'x1_regular', 0, overtime_hour[0], cat='Continuous')
x1_overtime = pulp.LpVariable(f'x1_overtime', 0, cat='Continuous')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(
    (machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)))
    for m in range(1, M)
)
labor_costs = (standard_cost * x1_regular) + (overtime_cost * x1_overtime)

problem += profit - costs - labor_costs

# Constraints
problem += (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) == x1_regular + x1_overtime)
problem += (x1_regular <= overtime_hour[0])

for m in range(1, M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m])

# Solve the problem
problem.solve()

# Extract results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print the results
print({
    "batches": batches_produced,
    "total_profit": total_profit
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')