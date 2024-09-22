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

# Problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Constants
P = len(data['prices'])
M = len(data['availability'])

# Decision Variables
batches = [pulp.LpVariable(f"batches_{p+1}", lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f"extra_time_{m+1}", lowBound=0, cat='Continuous') for m in range(M)]

# Objective Function
profit_term = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost_term = pulp.lpSum(
    data['machine_costs'][m] * (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m]
    ) + data['extra_costs'][m] * extra_time[m]
    for m in range(M)
)
problem += profit_term - cost_term

# Constraints
# Machine Time Availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Minimum Production Requirement
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Extra Time Limit
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')