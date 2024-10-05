from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Data provided in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Extracting parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

# Problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Variables
batches = [LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(P)]
extra_time = [LpVariable(f'extra_time_{m}', 0, max_extra[m], cat='Continuous') for m in range(M)]

# Objective
profit = lpSum([batches[p] * prices[p] for p in range(P)])
machine_cost = lpSum([(lpSum([batches[p] * time_required[m][p] for p in range(P)]) + extra_time[m]) * machine_costs[m] for m in range(M)])
extra_time_cost = lpSum([extra_time[m] * extra_costs[m] for m in range(M)])
objective = profit - machine_cost - extra_time_cost

problem += objective

# Constraints
for m in range(M):
    problem += lpSum([batches[p] * time_required[m][p] for p in range(P)]) <= availability[m] + extra_time[m]

# Solve
problem.solve()

# Results
result = {
    "batches": [batches[p].varValue for p in range(P)],
    "extra_time": [extra_time[m].varValue for m in range(M)],
    "total_profit": value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')