import pulp
import json

# Given data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Create the linear programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_hours = pulp.LpVariable.dicts("extra_hours", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (availability[m] + extra_hours[m]) for m in range(M)) - \
         pulp.lpSum(extra_costs[m] * extra_hours[m] for m in range(M))

problem += profit

# Constraints
# Machine Hour Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_hours[m] <= availability[m] + max_extra[m]

# Production Minimum Requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Extra Time Limits
for m in range(M):
    problem += extra_hours[m] <= max_extra[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')