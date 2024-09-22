import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

M = len(machine_costs)  # number of machines
P = len(prices)  # number of parts

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function: maximize total profit
total_profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)]) - \
               pulp.lpSum([(machine_costs[m] * (sum(time_required[m][p] * batches[p] for p in range(P)) / 100 + extra_time[m])) for m in range(M)]) 

problem += total_profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_part_{p}"

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum([(time_required[m][p] * batches[p] for p in range(P)]) / 100) + extra_time[m] <= availability[m] + max_extra[m]), f"Availability_machine_{m}"

# Solve the problem
problem.solve()

# Prepare the output
batches_result = [batches[p].varValue for p in range(P)]
extra_time_result = [extra_time[m].varValue for m in range(M)]
total_profit_value = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit_value
}

print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')