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

# Parameters
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat=pulp.LpInteger)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)])
costs = pulp.lpSum([data['machine_costs'][m] * 
                   (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + extra_time[m]) 
                   for m in range(M)])
extra_costs = pulp.lpSum([data['extra_costs'][m] * extra_time[m] for m in range(M)])

problem += profit - costs - extra_costs

# Constraints
for m in range(M):
    problem += (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + extra_time[m]
                <= data['availability'][m] + data['max_extra'][m])

for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve
problem.solve()

# Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')