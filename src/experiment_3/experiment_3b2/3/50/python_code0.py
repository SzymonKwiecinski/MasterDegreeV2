import pulp
import json

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Indices
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
e = pulp.LpVariable.dicts("extra_hours", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
           pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + e[m] * data['extra_costs'][m] for m in range(M))

# Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p], f"MinBatches_{p}"

for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m], f"AvailableTime_{m}"
    problem += e[m] <= data['max_extra'][m], f"MaxExtra_{m}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')