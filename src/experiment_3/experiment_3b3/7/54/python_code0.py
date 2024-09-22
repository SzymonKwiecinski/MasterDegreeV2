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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(data['NumParts'])]

# Labor cost for Machine 1
hours_machine_1 = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))
labor_cost_machine_1 = pulp.LpVariable('labor_cost_machine_1', lowBound=0, cat='Continuous')
problem += labor_cost_machine_1 == (
    pulp.lpSum([
        data['StandardCost'] * hours_machine_1,
        (data['OvertimeCost'] - data['StandardCost']) * (hours_machine_1 - data['OvertimeHour'][0])
    ]) * (hours_machine_1 > data['OvertimeHour'][0])
    + data['StandardCost'] * hours_machine_1 * (hours_machine_1 <= data['OvertimeHour'][0])
)

# Objective function
profit = pulp.lpSum(
    data['Prices'][p] * x[p] -
    pulp.lpSum(data['MachineCosts'][m] * data['TimeRequired'][m][p] / 100 * x[p]
               for m in range(data['NumMachines']))
    for p in range(data['NumParts'])
)
problem += profit - labor_cost_machine_1

# Constraints

# Machine Availability Constraints (machine 2 and 3)
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Minimum Production Requirements
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Results
batch_produced = [pulp.value(x[p]) for p in range(data['NumParts'])]
print(f'Batch produced: {batch_produced}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')