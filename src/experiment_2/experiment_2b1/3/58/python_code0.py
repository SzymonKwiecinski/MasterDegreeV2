import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Defining the problem
P = len(prices)
M = len(machine_costs)

problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize total profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))
problem += profit

# Constraints: Machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Setup time constraint for machine 1
for p in range(P):
    problem += batches[p] <= 1000 * setup_flags[p]  # If part is produced, it must be set up

# Setup time for machine 1
problem += pulp.lpSum(setup_flags[p] * setup_time[p] for p in range(P)) <= availability[0]

# Solve the problem
problem.solve()

# Prepare output
batches_output = [int(batches[p].varValue) for p in range(P)]
setup_flags_output = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_output,
    "setup_flags": setup_flags_output,
    "total_profit": total_profit
}

# Print the output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')