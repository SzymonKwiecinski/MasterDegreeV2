import pulp
import json

# Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Define model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)
e = pulp.LpVariable.dicts("e", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum(data['prices'][p] * x[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) + e[m]) for m in range(M)) - \
         pulp.lpSum(data['extra_costs'][m] * e[m] for m in range(M))

problem += profit

# Constraints
# Time constraints for each machine
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]), f"Time_Constraint_Machine_{m}"

# Minimum production constraints for each part
for p in range(P):
    problem += (x[p] >= data['min_batches'][p]), f"Min_Production_Constraint_Part_{p}"

# Extra time constraints for each machine
for m in range(M):
    problem += (0 <= e[m] <= data['max_extra'][m]), f"Extra_Time_Constraint_Machine_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')