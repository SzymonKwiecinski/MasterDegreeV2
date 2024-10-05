import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

P = len(data['prices'])     # Number of different parts
M = len(data['machine_costs'])  # Number of different machines

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, cat='Continuous') for m in range(M)]

# Objective Function
total_revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
total_machine_costs = pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M))
total_extra_costs = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))

profit = total_revenue - total_machine_costs - total_extra_costs
problem += profit

# Constraints
# Machine time constraint
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Minimum batch production requirement
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Maximum extra time purchase
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve
problem.solve()

# Output
batches_sol = [batches[p].varValue for p in range(P)]
extra_time_sol = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f"batches: {batches_sol}")
print(f"extra_time: {extra_time_sol}")
print(f"Total Profit (Objective Value): <OBJ>{total_profit}</OBJ>")