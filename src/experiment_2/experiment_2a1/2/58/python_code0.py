import pulp
import json

# Load the data from the given JSON format
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

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize total profit
profit = pulp.lpSum([(prices[p] * batches[p]) - 
                     pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for m in range(M)]) 
                     for p in range(P)])

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup time constraints for machine 1
for p in range(P):
    problem += batches[p] <= (1 - setup_flags[p]) * 10000  # Ensures batches are 0 if not set up
    if m == 0:  # Only for machine 1 which requires setup time
        problem += setup_flags[p] * setup_time[p] <= availability[0]  # Setup time should not exceed availability

# Solve the problem
problem.solve()

# Prepare the output
batches_output = [pulp.value(batches[p]) for p in range(P)]
setup_flags_output = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output results
result = {
    "batches": batches_output,
    "setup_flags": setup_flags_output,
    "total_profit": total_profit
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')