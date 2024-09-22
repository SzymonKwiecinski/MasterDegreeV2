import pulp
import json

# Input data in JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}")

# Problem parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define variables
P = len(prices)  # number of parts
M = len(availability)  # number of machines

batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective Function: Total Profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * batches[p] / 100) * machine_costs[m] for m in range(M)) - 
                     pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))) for p in range(P))

problem += profit, "Total_Profit"

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum((time_required[m][p] * batches[p] / 100) for p in range(P)) + extra_time[m] <= availability[m] + max_extra[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Output results
result_batches = [batches[p].varValue for p in range(P)]
result_extra_time = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

output = {
    "batches": result_batches,
    "extra_time": result_extra_time,
    "total_profit": total_profit
}

# The output can be printed or returned as needed
print(output)