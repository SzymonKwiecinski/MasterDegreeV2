import pulp
import json

# Data from the provided input
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

# Initialization of the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
num_parts = data['NumParts']
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum((data['Prices'][p] * batches[p] - 
                     pulp.lpSum((data['TimeRequired'][m][p] * batches[p] * data['MachineCosts'][m] 
                     for m in range(data['NumMachines'])))) 
                     for p in range(num_parts))

problem += profit

# Constraints for machine availability and production requirements
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) <= data['Availability'][m]

for p in range(num_parts):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Extract results
result_batches = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')