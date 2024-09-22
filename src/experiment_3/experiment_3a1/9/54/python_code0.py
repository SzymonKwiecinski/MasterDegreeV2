import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Define problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Variables
b = pulp.LpVariable.dicts("b", range(data['NumParts']), lowBound=data['MinBatches'], cat='Continuous')

# Objective function
profit = pulp.lpSum(data['Prices'][p] * b[p] for p in range(data['NumParts'])) - \
         pulp.lpSum(data['MachineCosts'][m] * (pulp.lpSum((data['TimeRequired'][m][p] / 100) * b[p] for p in range(data['NumParts']))) for m in range(data['NumMachines']))

labor_costs = []
for p in range(data['NumParts']):
    labor_expr = pulp.lpSum(b[p] * (data['TimeRequired'][0][p] / 100))
    labor_costs.append(pulp.lpSum((data['StandardCost'] * labor_expr, 
                                    data['OvertimeCost'] * (labor_expr - data['OvertimeHour'][0]) + data['StandardCost'] * data['OvertimeHour'][0])))

# Add labor costs to the objective
problem += profit - pulp.lpSum(labor_costs)

# Constraints
# Machine Availability constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum((data['TimeRequired'][m][p] / 100) * b[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Machine_Availability_{m}"

# Solve problem
problem.solve()

# Output result
result = {f'b_{p}': b[p].varValue for p in range(data['NumParts'])}
result['total_profit'] = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{result["total_profit"]}</OBJ>')