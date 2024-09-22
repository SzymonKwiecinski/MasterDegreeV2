import pulp
import json

# Given data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

# Extract the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize profit
profit_expression = pulp.lpSum(prices[p] * batches[p] for p in range(P))
cost_expression = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) / 100 for m in range(M))
problem += profit_expression - cost_expression

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f'Availability_Constraint_{m}'

for p in range(P):
    problem += batches[p] <= 100 * setup_flags[p], f'Batch_Setup_Constraint_{p}'

# Solve the problem
problem.solve()

# Prepare the output
batches_result = [pulp.value(batches[p]) for p in range(P)]
setup_flags_result = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output_data = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')