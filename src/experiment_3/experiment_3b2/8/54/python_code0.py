import pulp
import json

# Input data
data_json = '''{
    "NumMachines": 3,
    "NumParts": 4,
    "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "MachineCosts": [160, 10, 15],
    "Availability": [200, 300, 500],
    "Prices": [570, 250, 585, 430],
    "MinBatches": [10, 10, 10, 10],
    "StandardCost": 20,
    "OvertimeCost": 30,
    "OvertimeHour": [400, 400, 300]
}'''

data = json.loads(data_json)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['NumParts']), lowBound=0, cat='Continuous')

# Objective function components
profit_terms = [data['Prices'][p] * x[p] for p in range(data['NumParts'])]
cost_terms = [data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])]
labor_cost = pulp.lpSum(data['StandardCost'] * pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))) if pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) <= data['OvertimeHour'][0] else \
    data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'][0] * (pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) - data['OvertimeHour'][0])

# Full objective function
problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms) - labor_cost, "Total_Profit"

# Constraints
# Demand constraints
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')