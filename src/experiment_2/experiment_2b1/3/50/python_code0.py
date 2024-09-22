import pulp
import json

# Data input
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

# Extract data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for the number of batches of each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Decision variables for the extra hours purchased for each machine
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function: Total profit
total_profit = pulp.lpSum([(prices[p] * batches[p]) - 
                            pulp.lpSum([time_required[m][p] * machine_costs[m] * (batches[p] / 100) 
                                         for m in range(M)]) 
                            for p in range(P)])

# Add the cost of extra time for each machine
total_extra_cost = pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(M)])
problem += total_profit - total_extra_cost, "Total_Profit"

# Constraints for minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * (batches[p] / 100) for p in range(P)]) + extra_time[m] <= availability[m] + max_extra[m], f"MachineAvailability_{m}"

# Solve the problem
problem.solve()

# Preparing the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "extra_time": [pulp.value(extra_time[m]) for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

# Print result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')