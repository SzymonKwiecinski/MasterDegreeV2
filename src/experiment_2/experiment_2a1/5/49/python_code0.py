import json
import pulp

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting parameters from the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for batches of each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function: Maximize Profit
total_profit = pulp.lpSum([(prices[p] - pulp.lpSum([time_required[m][p] * machine_costs[m] for m in range(M)])) * batches[p] for p in range(P)])
problem += total_profit, "Total_Profit"

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Availability constraints (shared for the last two machines)
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Prepare the output
batches_output = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_output,
    "total_profit": total_profit_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')