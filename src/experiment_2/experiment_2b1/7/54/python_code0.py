import pulp
import json

# Input Data
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

# Number of Machines and Parts
M = data['NumMachines']
P = data['NumParts']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize profit
profit = pulp.lpSum((data['Prices'][p] * batches[p] - 
                     pulp.lpSum((data['TimeRequired'][m][p]) * batches[p] / 100 * data['MachineCosts'][m] 
                     for m in range(M))) for p in range(P))
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(P)) <= data['Availability'][m]

# Constraints for minimum batch production
for p in range(P):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Output the results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')