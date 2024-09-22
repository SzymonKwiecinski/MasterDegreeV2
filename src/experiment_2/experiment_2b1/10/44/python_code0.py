import json
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, LpStatusOptimal

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting data from the JSON object
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the LP problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Define variables for batches
batches = LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = lpSum((prices[p] * batches[p]) for p in range(P)) - lpSum(
    (machine_costs[m] * lpSum((time_required[m][p] / 100) * batches[p] for p in range(P))) for m in range(M))
)

problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine availability constraints
for m in range(M):
    problem += lpSum((time_required[m][p] / 100) * batches[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Prepare the output
batches_output = [batches[p].varValue for p in range(P)]
total_profit = value(problem.objective)

output = {
    "batches": batches_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')