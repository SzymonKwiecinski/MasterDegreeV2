import pulp

# Data from the problem
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

# Unpack the data
num_machines = data['NumMachines']
num_parts = data['NumParts']
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

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(num_parts)]

# Objective function
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts))

def calculate_costs(m):
    part_use = pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts))
    if m == 0:
        # Handle machine 1's special cost condition with overtime
        standard_hours = pulp.lpMin(part_use, overtime_hour[m])
        overtime_hours = part_use - standard_hours
        return standard_hours * standard_cost + overtime_hours * overtime_cost
    else:
        return part_use * machine_costs[m]

total_cost = pulp.lpSum(calculate_costs(m) for m in range(num_machines))
problem += total_revenue - total_cost

# Constraints for machine 2 and 3 availability
for m in range(1, num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m]

# Solve the problem
problem.solve()

# Output the results
output = {
    "batches": [pulp.value(batches[p]) for p in range(num_parts)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')