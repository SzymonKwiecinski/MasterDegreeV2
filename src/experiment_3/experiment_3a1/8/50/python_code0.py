import pulp
import json

data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}")

# Define the data based on the imported JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Create a linear programming problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define sets
P = len(prices)  # Number of different parts
M = len(machine_costs)  # Number of different machines

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m]) for m in range(M)) - \
           pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m] <= availability[m] + max_extra[m])

# Minimum Batches Requirement
for p in range(P):
    problem += (batches[p] >= min_batches[p])

# Solve the problem
problem.solve()

# Output Results
batches_solution = [batches[p].varValue for p in range(P)]
extra_time_solution = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches_solution}')
print(f' (Extra Time Purchased): {extra_time_solution}')
print(f' (Total Profit): <OBJ>{total_profit}</OBJ>')