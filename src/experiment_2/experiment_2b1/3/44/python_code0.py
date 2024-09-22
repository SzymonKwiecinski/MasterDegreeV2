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

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Problem setup
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[p] * batches[p]) for p in range(P))
costs = pulp.lpSum((machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P))) for m in range(M))
total_profit = profit - costs
problem += total_profit

# Constraints for minimum batch production
for p in range(P):
    problem += (batches[p] >= min_batches[p]), f"MinBatches_{p}"

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]), f"MachineAvailability_{m}"

# Solve the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit_value
}

print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')