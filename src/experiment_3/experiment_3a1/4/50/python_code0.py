import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Model
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, upBound=data['max_extra'], cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
           pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M)) - \
           pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m], f"Time_Constraint_Machine_{m+1}"

for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_Part_{p+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')