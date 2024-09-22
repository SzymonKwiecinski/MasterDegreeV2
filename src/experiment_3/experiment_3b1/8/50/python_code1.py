import pulp
import json

# Data initialization from JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Problem setup
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Variables
P = len(data['prices'])
M = len(data['machine_costs'])

batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m]) for m in range(M))
extra_cost = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))

problem += profit - cost - extra_cost

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m]), f"Machine_Availability_{m}"

# Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_{p}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    print(f'Batches of part {p + 1}: {batches[p].varValue}')
for m in range(M):
    print(f'Extra time for machine {m + 1}: {extra_time[m].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')