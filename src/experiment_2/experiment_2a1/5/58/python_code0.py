import json
import pulp

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Problem setup
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Integer') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flag_{p}', cat='Binary') for p in range(P)]

# Objective function: Maximize total profit
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)]) - \
         pulp.lpSum([batches[p] * setup_flags[p] * setup_time[p] * machine_costs[0] for p in range(P)]) - \
         pulp.lpSum([batches[p] * sum(time_required[m][p] * machine_costs[m] for m in range(M)) for p in range(P)])

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([batches[p] * time_required[m][p] for p in range(P)]) <= availability[m], f"Availability_Constraint_Machine_{m}"

for p in range(P):
    problem += batches[p] <= setup_flags[p] * (pulp.LpVariable('inf', lowBound=0)), f"Setup_Constraint_Part_{p}"

# Solve the problem
problem.solve()

# Collecting results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')