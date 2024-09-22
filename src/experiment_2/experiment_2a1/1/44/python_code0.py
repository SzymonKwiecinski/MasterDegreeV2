import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extracting data from input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables for the number of batches for each part
num_parts = len(prices)
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function: maximize total profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum(time_required[m][p] * machine_costs[m] for m in range(len(machine_costs))) * batches[p]) 
                    for p in range(num_parts))
                    
problem += profit

# Constraints for minimum batches
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Machine availability constraints
for m in range(len(availability)):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m]), f"Availability_Constraint_{m}"

# Solve the problem
problem.solve()

# Collecting results
result_batches = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')