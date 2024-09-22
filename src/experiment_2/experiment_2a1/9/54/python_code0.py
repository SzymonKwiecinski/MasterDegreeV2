import pulp
import json

# Data from the input
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

# Extract data
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')

# Objective function: maximize profit
problem += pulp.lpSum(prices[p] * batches[p] - 
                      pulp.lpSum((time_required[m][p] * (standard_cost * 
                      (pulp.lpSum(batches[p] * 100) / availability[m]) + 
                      overtime_cost * (pulp.lpSum(batches[p] * 100) / availability[m] - overtime_hour[m])))) 
                      for m in range(M)) for p in range(P))

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Collect results
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

# Print output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')