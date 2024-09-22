import pulp
import json

# Input data
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

# Problem variables
P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(time_required[m][p] * machine_costs[m] * (batches[p] / 100) 
                    for p in range(P) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraint (shared between M and M-1)
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p}"

# Solve the problem
problem.solve()

# Prepare output
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print output
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')