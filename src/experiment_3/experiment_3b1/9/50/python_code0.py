import pulp
import json

# Input data
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}")

# Create the Linear Program
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Define variables
P = len(data['prices'])
M = len(data['machine_costs'])

batches = [pulp.LpVariable(f'batches_{p}', lowBound=0) for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(M)]

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M))
extra_cost = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))

problem += profit - cost - extra_cost, "Total Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m], f"Machine_{m}_Capacity"

for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output results
batches_produced = {f'batches_{p}': batches[p].varValue for p in range(P)}
extra_hours_purchased = {f'extra_time_{m}': extra_time[m].varValue for m in range(M)}
total_profit = pulp.value(problem.objective)

print(batches_produced)
print(extra_hours_purchased)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')