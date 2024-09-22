import pulp

# Data from JSON
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
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p]) for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0) for m in range(M)]

# Objective Function
profit = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) -
    pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                                           data['extra_costs'][m] * extra_time[m]) for m in range(M))
)
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]
    problem += extra_time[m] <= data['max_extra'][m]

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')