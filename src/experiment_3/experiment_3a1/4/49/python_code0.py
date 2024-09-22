import pulp
import json

# Data from the provided JSON
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Model parameters
P = len(data['min_batches'])  # number of parts
M = len(data['machine_costs'])  # number of machines

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
           pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

# Constraints
# Production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Shared availability for Machine M and Machine M-1
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1] + availability[M-2]

# Solve the problem
problem.solve()

# Output the results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'batches = {batches_solution}')
print(f'total_profit = {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')