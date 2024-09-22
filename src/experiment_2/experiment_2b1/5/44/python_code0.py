import json
import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * machine_costs[m] / 100) * batches[p] 
                                 for m in range(M))) 
                     for p in range(P))

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Constraints for minimum batches for each part
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')