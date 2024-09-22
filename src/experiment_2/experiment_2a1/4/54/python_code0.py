import pulp
import json

# Input data
data = {'NumMachines': 3, 'NumParts': 4, 
        'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'MachineCosts': [160, 10, 15], 
        'Availability': [200, 300, 500], 
        'Prices': [570, 250, 585, 430], 
        'MinBatches': [10, 10, 10, 10], 
        'StandardCost': 20, 
        'OvertimeCost': 30, 
        'OvertimeHour': [400, 400, 300]}

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
num_parts = data['NumParts']
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function (profit = revenue - cost)
profit = pulp.lpSum(data['Prices'][p] * batches[p] - 
                    pulp.lpSum(data['MachineCosts'][m] * data['TimeRequired'][m][p] * batches[p] / 100 
                    for m in range(data['NumMachines']))
                    for p in range(num_parts))

problem += profit

# Constraints
for p in range(num_parts):
    problem += batches[p] >= data['MinBatches'][p]  # Minimum batches per part

for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) <= data['Availability'][m]  # Machine availability

# Solve the problem
problem.solve()

# Output results
batches_output = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')