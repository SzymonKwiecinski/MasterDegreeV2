from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value
import json

# Input Data
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

P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Initialize the problem
problem = LpProblem("Auto_Parts_Production", LpMaximize)

# Decision Variables
batches = [LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]

# Calculate profit
revenue = lpSum(data['prices'][p] * batches[p] for p in range(P))

# Setup cost calculation for Machine 1 based on outsourcing conditions
# Considering Machine 1 has different cost structure
machine_usage_1 = lpSum(data['time_required'][0][p] * batches[p] for p in range(P))
regular_cost = data['standard_cost'] * min(machine_usage_1, data['overtime_hour'])
overtime_cost = data['overtime_cost'] * max(0, machine_usage_1 - data['overtime_hour'])

cost_1 = regular_cost + overtime_cost

# Calculate other machines costs
costs = [cost_1]
for m in range(1, M):
    machine_usage = lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
    costs.append(data['machine_costs'][m] * machine_usage)

total_cost = lpSum(costs)

profit = revenue - total_cost

# Objective: Maximize profit
problem += profit

# Constraints
# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine time availability constraint (Machine 1 availability condition is disregarded)
for m in range(1, M):
    problem += lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Minimum profit constraint
problem += profit >= data['min_profit']

# Solve the problem
problem.solve()

# Output results
output = {
    "batches": [int(value(batches[p])) for p in range(P)],
    "total_profit": value(profit)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')