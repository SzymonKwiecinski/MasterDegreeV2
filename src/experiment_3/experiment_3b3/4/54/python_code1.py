import pulp

# Data extracted from JSON
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

# Problem setup
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

# Calculate total_time for labor cost
total_time = sum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))

# Labor Costs calculation
overtime_hours = data['OvertimeHour']
labor_costs = pulp.LpVariable("labor_costs", cat='Continuous')
problem += labor_costs

# Add piecewise conditions for labor costs
for m in range(data['NumMachines']):
    max_overtime = data['OvertimeHour'][m]
    problem += (labor_costs >= data['StandardCost'] * total_time - (data['StandardCost'] - data['OvertimeCost']) * max_overtime)
    problem += (labor_costs <= data['StandardCost'] * max_overtime + data['OvertimeCost'] * (total_time - max_overtime))

# Objective function
profit = (
    sum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) -
    sum(data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines'])) -
    labor_costs
)
problem += profit

# Constraints
for m in range(data['NumMachines']):  # Constraints for m from 0 to M-1
    machine_limit = sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts']))
    problem += machine_limit <= data['Availability'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')