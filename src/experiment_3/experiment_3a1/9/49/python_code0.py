import pulp
import json

# Data in JSON format
data_json = '''{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}'''
data = json.loads(data_json)

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(M)) for p in range(P))
problem += profit

# Constraints
# Machine Availability Constraints
availability_constraint = pulp.lpSum(time_required[m][p] * batches[p] for p in range(P) for m in range(M))
problem += (availability_constraint <= pulp.lpSum(availability[m] for m in range(M))), "Machine_Availability"

# Minimum Batch Production Constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p]), f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    print(f'batches_{p}: {batches[p].varValue}')

# Total profit
total_profit = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')