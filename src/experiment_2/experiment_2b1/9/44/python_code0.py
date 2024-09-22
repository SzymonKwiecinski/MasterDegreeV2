import pulp
import json

# Input data in json format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Batches of each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective function: total profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * machine_costs[m]) * batches[p] for m in range(M))) 
                     for p in range(P))
                    )
problem += profit

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m])

# Constraints for minimum batches
for p in range(P):
    problem += (batches[p] >= min_batches[p])

# Solve the problem
problem.solve()

# Prepare results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')