import pulp
import json

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

# Initialize the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(data['NumParts']), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) 
cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
problem += profit - cost

# Constraints
# Machine availability constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Minimum production requirements
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

# Define labor cost for Machine 1
hours_m1 = pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))
labor_cost_m1 = data['StandardCost'] * hours_m1

# Handling overtime
overtime_hours_m1 = hours_m1 - data['OvertimeHour'][0]
problem += labor_cost_m1 <= (data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (overtime_hours_m1)) if hours_m1 > data['OvertimeHour'][0] else data['StandardCost'] * hours_m1

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')