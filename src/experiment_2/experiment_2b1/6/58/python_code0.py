import json
import pulp

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum((prices[p] * batches[p]) for p in range(P)) - \
         pulp.lpSum((machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))) for m in range(M))

problem += profit

# Constraints for each machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"availability_constraint_machine_{m}"

# Setup time constraint for machine 1
for p in range(P):
    if p == 0:  # Assuming setup time is only for part 1
        problem += batches[p] <= setup_flags[p] * (availability[0] // (setup_time[p] + sum(time_required[m][p] for m in range(M)))), f"setup_constraint_part_{p}"

# Solve the problem
problem.solve()

# Collect results
result_batches = [pulp.value(batches[p]) for p in range(P)]
result_setup_flags = [pulp.value(setup_flags[p]) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": result_batches,
    "setup_flags": result_setup_flags,
    "total_profit": total_profit
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')