import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

# Problem setup
P = len(data['prices'])
M = len(data['machine_costs'])
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) \
         - pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) / 100 + extra_time[m]) for m in range(M))
problem += profit

# Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]  # Minimum batch constraints

for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) / 100 <= data['availability'][m] + extra_time[m]  # Machine time constraints
    problem += extra_time[m] <= data['max_extra'][m]  # Extra time limits

# Solve the problem
problem.solve()

# Output results
batches_produced = [pulp.value(batches[p]) for p in range(P)]
extra_time_hours = [pulp.value(extra_time[m]) for m in range(M)]
total_profit = pulp.value(problem.objective)

# Output formatting
output = {
    "batches": batches_produced,
    "extra_time": extra_time_hours,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')