import pulp
import json

# Load data from JSON
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Problem setup
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['NumParts']), lowBound=0, cat='Continuous')
h1 = pulp.LpVariable("h1", lowBound=0)
h1_overtime = pulp.LpVariable("h1_overtime", lowBound=0)

# Objective Function
profit = pulp.lpSum([data['Prices'][p] * x[p] for p in range(data['NumParts'])])
cost = pulp.lpSum([data['MachineCosts'][m] * pulp.lpSum([data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])]) for m in range(1, data['NumMachines'])])
standard_cost = data['StandardCost'] * h1
overtime_cost = data['OvertimeCost'] * h1_overtime
problem += profit - cost - standard_cost - overtime_cost

# Constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum([data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])]) <= data['Availability'][m], f"Machine_{m}_availability"

problem += pulp.lpSum([data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])]) == h1 + h1_overtime, "Machine_1_time_allocation"
problem += h1 <= data['OvertimeHour'][0], "Standard_time_limit_Machine_1"

for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"Min_batches_part_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')