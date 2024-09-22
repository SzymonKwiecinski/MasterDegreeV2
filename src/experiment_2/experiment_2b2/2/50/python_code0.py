import pulp

# Extracting data from JSON
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}

# Decision Variables
P = len(data["prices"])
M = len(data["availability"])
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data["min_batches"][p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data["max_extra"][m], cat='Continuous') for m in range(M)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
total_revenue = pulp.lpSum([data["prices"][p] * batches[p] for p in range(P)])
total_machine_costs = pulp.lpSum([(data["machine_costs"][m] * (pulp.lpSum([data["time_required"][m][p] * batches[p] for p in range(P)]))) + (data["extra_costs"][m] * extra_time[m]) for m in range(M)])
total_profit = total_revenue - total_machine_costs
problem += total_profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([data["time_required"][m][p] * batches[p] for p in range(P)]) <= data["availability"][m] + extra_time[m]

# Solving the Problem
problem.solve()

# Output
batches_produced = [pulp.value(batches[p]) for p in range(P)]
extra_hours = [pulp.value(extra_time[m]) for m in range(M)]
total_profit_value = pulp.value(total_profit)

output = {
    "batches": batches_produced,
    "extra_time": extra_hours,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')