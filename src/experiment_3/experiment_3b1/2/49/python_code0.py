import pulp
import json

# Load data
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}")

# Parameters from data
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']      # available_m
prices = data['prices']                  # price_p
min_batches = data['min_batches']        # min_batches_p

# Define problem
P = len(prices)  # Number of parts
M = len(availability)  # Number of machines
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit - cost

# Constraints
# Production Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Shared Availability for Machine M and M-1
problem += pulp.lpSum(time_required[M-1][p] * batches[p] for p in range(P)) + pulp.lpSum(time_required[M-2][p] * batches[p] for p in range(P)) <= availability[M-1] + availability[M-2]

# Solve the problem
problem.solve()

# Output results
batches_values = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches: {batches_values}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')