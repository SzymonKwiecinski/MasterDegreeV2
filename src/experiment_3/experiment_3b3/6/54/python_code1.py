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

# Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
batches = {p: pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Integer') for p in range(data['NumParts'])}

# Objective Function
total_revenue = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts']))
total_machine_cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))

# Handle overtime cost for machine 1
time_machine_1 = pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))
standard_cost_part = data['StandardCost'] * pulp.lpSum([pulp.lpMin(time_machine_1, data['OvertimeHour'][0])])
overtime_cost_part = data['OvertimeCost'] * (time_machine_1 - data['OvertimeHour'][0])
overtime_cost = pulp.lpMax(overtime_cost_part, 0)

problem += total_revenue - total_machine_cost - (standard_cost_part + overtime_cost)

# Constraints
# Machine availability
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve
problem.solve()

# Output the results
for p in range(data['NumParts']):
    print(f'Batches of part {p+1}: {pulp.value(batches[p])}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')