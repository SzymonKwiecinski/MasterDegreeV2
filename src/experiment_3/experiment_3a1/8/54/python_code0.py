import pulp
import json

# Input data
data = json.loads('''{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}''')

# Initialize the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Variables
batches = pulp.LpVariable.dicts("Batches", range(data['NumParts']), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) \
         - pulp.lpSum(pulp.lpSum(data['TimeRequired'][m][p] * batches[p] * data['MachineCosts'][m]
                                   for p in range(data['NumParts'])) for m in range(data['NumMachines']))

# Labor costs
labor_costs = []
for p in range(data['NumParts']):
    hours = pulp.lpSum(data['TimeRequired'][0][p] * batches[p])
    labor_cost = pulp.lpSum([
        data['StandardCost'] * hours if hours <= data['OvertimeHour'][0] else
        data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (hours - data['OvertimeHour'][0])
    ])
    labor_costs.append(labor_cost)

# Add labor costs to objective
total_labor_costs = pulp.lpSum(labor_costs)
problem += profit - total_labor_costs, "Total_Profit"

# Capacity constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Capacity_Constraint_{m+1}"

# Minimum production requirements
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p], f"Min_Batches_Constraint_{p+1}"

# Solve the problem
problem.solve()

# Output results
for p in range(data['NumParts']):
    print(f'Batches produced for part {p+1}: {batches[p].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')