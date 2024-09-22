import pulp
import json

# Data in JSON format
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

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("Batches", range(1, data['NumParts'] + 1), lowBound=0)

# Calculate time_1 and Cost_1
time_1 = pulp.lpSum(data['TimeRequired'][0][p-1] * x[p] for p in range(1, data['NumParts'] + 1))

Cost_1 = pulp.lpSum(
    [data['StandardCost'] * time_1 if time_1 <= data['OvertimeHour'][0] else 
     data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (time_1 - data['OvertimeHour'][0])]
)

# Objective Function
profit = pulp.lpSum(data['Prices'][p-1] * x[p] for p in range(1, data['NumParts'] + 1)) \
         - pulp.lpSum(
             pulp.lpSum(data['TimeRequired'][m-1][p-1] * x[p] * data['MachineCosts'][m] 
                        for p in range(1, data['NumParts'] + 1))
             for m in range(2, data['NumMachines'] + 1)
         ) - Cost_1

problem += profit

# Constraints
for m in range(2, data['NumMachines'] + 1):
    problem += pulp.lpSum(data['TimeRequired'][m-1][p-1] * x[p] for p in range(1, data['NumParts'] + 1)) <= data['Availability'][m-1]

for p in range(1, data['NumParts'] + 1):
    problem += x[p] >= data['MinBatches'][p-1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')