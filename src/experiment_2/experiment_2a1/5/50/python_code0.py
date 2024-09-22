import json
import pulp

# Data from the input
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

# Parse data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (availability[m] + extra_time[m]) * (pulp.lpSum(time_required[m][p] for p in range(P)) / 100) for m in range(M))

problem += profit

# Constraints for batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Machine time constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], f"MachineAvailability_{m}"

# Max extra time constraints
for m in range(M):
    problem += extra_time[m] <= max_extra[m], f"MaxExtra_{m}"

# Solve the problem
problem.solve()

# Prepare the output
batches_values = [int(batches[p].value()) for p in range(P)]
extra_time_values = [int(extra_time[m].value()) for m in range(M)]
total_profit = pulp.value(problem.objective)

# Output Result
output = {
    "batches": batches_values,
    "extra_time": extra_time_values,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')