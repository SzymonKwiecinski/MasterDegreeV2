import pulp

# Define the data
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
M, P = data['NumMachines'], data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p+1}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(time_required[m][p] * batches[p] * machine_costs[m] for m in range(1, M) for p in range(P))

# Machine 1 constraints for labor costs
labor_hours = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
labor_cost = (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) * standard_cost +
              pulp.lpSum(pulp.lpMax([0, labor_hours - overtime_hour[0]]) * (overtime_cost - standard_cost)))

# Objective: Maximize profit
problem += revenue - costs - labor_cost

# Constraints for Machines 2 and 3
for m in range(1, M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m-1], f"Machine_{m+1}_Availability"

# Solve the problem
problem.solve()

# Extract results
result_batches = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')