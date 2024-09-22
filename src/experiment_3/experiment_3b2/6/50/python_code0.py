import pulp
import json

# Data provided in JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}")

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
P = len(data['prices'])
M = len(data['machine_costs'])

# x_p: Number of batches of part p produced
x = pulp.LpVariable.dicts("Batch", range(P), lowBound=0)

# e_m: Additional hours purchased for machine m
e = pulp.LpVariable.dicts("ExtraHours", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + e[m] * data['extra_costs'][m] for m in range(M))

problem += profit

# Constraints
# Machine time constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

# Minimum batches constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Extra hours constraints
for m in range(M):
    problem += e[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')