from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Data from the problem
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Unpack data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

M = len(machine_costs)
P = len(prices)

# Define the problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Variables
batches = [LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]
extra_time = [LpVariable(f'extra_time_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective function: maximize profit
profit = lpSum(prices[p] * batches[p] for p in range(P))
machine_cost = lpSum(
    (lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m]) * machine_costs[m]
    for m in range(M)
)
extra_time_cost = lpSum(extra_time[m] * extra_costs[m] for m in range(M))

# Total profit
total_profit = profit - machine_cost - extra_time_cost
problem += total_profit

# Constraints
for m in range(M):
    problem += lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], f"Availability_Machine_{m}"

# Solve the problem
problem.solve()

# Output the solution
output = {
    "batches": [value(batches[p]) for p in range(P)],
    "extra_time": [value(extra_time[m]) for m in range(M)],
    "total_profit": value(total_profit)
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')