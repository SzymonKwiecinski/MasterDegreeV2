import pulp
import json

# Input data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Model initialization
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts']))
total_cost = pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(data['NumMachines']))
hours = pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for m in range(data['NumMachines']) for p in range(data['NumParts']))
labor_cost = pulp.lpSum(data['StandardCost'] * pulp.lpMin(hours[m], data['OvertimeHour'][m]) for m in range(data['NumMachines'])) + \
             pulp.lpSum(data['OvertimeCost'] * (hours[m] - data['OvertimeHour'][m]) for m in range(data['NumMachines']) if hours[m] > data['OvertimeHour'][m])
objective_function = total_revenue - total_cost - labor_cost

problem += objective_function

# Constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(data['NumParts'])]
print(f'Batches: {batches_result}')
print(f'Total Profit: <OBJ>{pulp.value(problem.objective)}</OBJ>')