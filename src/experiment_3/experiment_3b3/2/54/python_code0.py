import pulp

# Data
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
batches = [pulp.LpVariable(f'b_{p}', lowBound=0, cat='Continuous') for p in range(data['NumParts'])]

# Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts']))

machine_cost = 0
for m in range(data['NumMachines']):
    total_time_m = pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts']))
    if m == 0:
        standard_cost = data['StandardCost'] * total_time_m
        overtime = total_time_m - data['OvertimeHour'][m]
        overtime_cost = data['OvertimeCost'] * overtime
        machine_cost += pulp.LpVariable("cost_1", lowBound=0) * (standard_cost + pulp.lpSum(overtime_cost if total_time_m > data['OvertimeHour'][m] else 0))
    else:
        machine_cost += data['MachineCosts'][m] * total_time_m

problem += profit - machine_cost

# Constraints

# Machine Availability Constraints
for m in range(data['NumMachines']):
    problem += (pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]), f"Machine_Availability_{m}"

# Minimum Production Requirements
for p in range(data['NumParts']):
    problem += (batches[p] >= data['MinBatches'][p]), f"Min_Production_{p}"

# Solve
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')