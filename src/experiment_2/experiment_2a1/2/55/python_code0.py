import json
import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define variables
P = len(data['min_batches'])  # Number of parts
M = len(data['time_required'])  # Number of machines

# Decision variables: number of batches produced
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum([(data['prices'][p] * batches[p] - 
                       pulp.lpSum([data['machine_costs'][m] * data['time_required'][m][p] * batches[p] / 100.0 
                                    for m in range(M)])) 
                      for p in range(P)])
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m]

# Calculate total labor cost for Machine 1
# Note: Machine 1 requires special handling for labor costs
problem += (pulp.lpSum([data['time_required'][0][p] * batches[p] for p in range(P)]) <= data['availability'][0] + 
              (data['overtime_hour'] - data['availability'][0]) 
              if data['overtime_hour'] > data['availability'][0] else 0)

# Profit must exceed minimum profit requirement
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Result extraction
batches_result = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output formatted result
result = {
    "batches": batches_result,
    "total_profit": total_profit
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')