import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}

# Extract data from the json-like format
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
P = len(prices)  # number of parts
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: maximize profit
profit = pulp.lpSum((prices[p] * batches[p]) for p in range(P)) - \
         pulp.lpSum((machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P))) for m in range(len(machine_costs)))

problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine availability constraints
for m in range(len(availability)):
    problem += pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Collect results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Prepare the output
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')