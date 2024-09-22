import pulp

# Data from input
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

# Unpack data
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p+1}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function
# Revenue: Sum(price[p] * batches[p])
# Cost for machine 1 (outsourced): Sum(time[0][p] * batches[p] * standard_cost) for time <= overtime_hour
# plus overtime_cost for time > overtime_hour
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_1_time = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))

cost_machine_1 = pulp.lpSum(
    time_required[0][p] * batches[p] * standard_cost if time_required[0][p] * batches[p] <= overtime_hour[0] else (overtime_hour[0] * standard_cost + (time_required[0][p] * batches[p] - overtime_hour[0]) * overtime_cost)
    for p in range(P)
)

# Costs for other machines
cost_other_machines = pulp.lpSum(
    pulp.lpSum(time_required[m][p] * batches[p] * machine_costs[m] for p in range(P))
    for m in range(1, M)
)

total_profit = revenue - (cost_machine_1 + cost_other_machines)
problem += total_profit

# Constraints
# Machine availability constraints for machines 2-M
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Output the results
result = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(total_profit)
}

print(f'Result: {result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')