from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpStatus
import json

# Load the data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)
M = len(machine_costs)

# Define the linear programming problem
problem = LpProblem("AutoPartsManufacturer", LpMaximize)

# Decision Variables
batches = [LpVariable(f'batches_{p}', lowBound=min_batches[p]) for p in range(P)]

# Objective Function
total_revenue = lpSum(prices[p] * batches[p] for p in range(P))
total_cost = lpSum(machine_costs[m] * lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += total_revenue - total_cost

# Constraints
# Machine availability constraints
for m in range(M):
    problem += lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Output results
print(f'Status: {LpStatus[problem.status]}')
for p in range(P):
    print(f'Batches of part {p+1}: {batches[p].varValue}')
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')