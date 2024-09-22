import pulp
import json

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

# Problem Initialization
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Variables
b = pulp.LpVariable.dicts("b", range(data['NumParts']), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts']))
costs = pulp.lpSum(data['MachineCosts'][m] * (1/100) * pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
labor_cost_machine_1 = pulp.lpSum(pulp.lpSum(data['StandardCost'] * (data['TimeRequired'][0][p] * b[p]) if (data['TimeRequired'][0][p] * b[p]) <= data['OvertimeHour'][0] else 
                                                  (data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * ((data['TimeRequired'][0][p] * b[p]) - data['OvertimeHour'][0])) for p in range(data['NumParts']))

# Combine objective components
problem += profit - costs - labor_cost_machine_1, "TotalProfit"

# Constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * b[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Availability_Constraint_Machine_{m+1}"

for p in range(data['NumParts']):
    problem += b[p] >= data['MinBatches'][p], f"MinBatches_Constraint_Part_{p+1}"

# Solve the problem
problem.solve()

# Output
for p in range(data['NumParts']):
    print(f'Number of batches produced for part {p+1}: {b[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')