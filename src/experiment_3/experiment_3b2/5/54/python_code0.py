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

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0, cat='Continuous')
x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')  # Standard labor hours for machine 1
y1 = pulp.LpVariable("y1", lowBound=0, cat='Continuous')  # Overtime labor hours for machine 1

# Objective Function
profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(data['NumParts'])) \
        - pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])) \
        - (data['StandardCost'] * x1 + data['OvertimeCost'] * y1)

problem += profit

# Constraints
# Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Labor hours constraint for machine 1
problem += x1 + y1 >= pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))

# Standard hours constraint for machine 1
problem += x1 <= data['OvertimeHour'][0]

# Minimum batches constraints
for p in range(data['NumParts']):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')