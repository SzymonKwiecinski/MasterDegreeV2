import pulp
import json

# Data extraction from JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Problem creation
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Variables
P = len(data['prices'])
M = len(data['machine_costs'])
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
e = pulp.LpVariable.dicts("extra_hours", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum(data['prices'][p] * b[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) + e[m]) for m in range(M)) - \
         pulp.lpSum(data['extra_costs'][m] * e[m] for m in range(M))

problem += profit

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * b[p] for p in range(P)) + e[m] <= 
                 data['availability'][m] + data['max_extra'][m])

for p in range(P):
    problem += (b[p] >= data['min_batches'][p])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')