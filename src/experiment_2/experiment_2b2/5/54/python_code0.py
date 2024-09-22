import pulp

# Data input
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

# Extract data
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

# Create a LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of batches to produce for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective Function: Maximize the total profit
profit = pulp.lpSum([
    prices[p] * batches[p]
    for p in range(P)
])

costs = 0

# Machine 1 cost accounting separately with overtime consideration
machine_1_hours = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
for m in range(1, M):
    costs += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) * machine_costs[m]
overtime_used = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) - overtime_hour[0]
overtime_cost_part = pulp.lpSum([pulp.LpVariable(f'overtime_{m}', lowBound=0, cat='Continuous') for m in range(1, M)]) * overtime_cost
overtime_cost_part += (pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)]) - overtime_hour[0]) * overtime_cost
standard_cost_part = overtime_hour[0] * standard_cost

costs += pulp.lpSum([
    pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) * machine_costs[m]
    for m in range(1, M) 
]) + standard_cost_part + overtime_cost_part

# Total Profit
problem += profit - costs

# Constraints
for m in range(1, M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

problem.solve()

# Output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')