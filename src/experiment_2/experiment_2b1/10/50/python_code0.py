import pulp
import json

# Input data in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Extract the input data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Number of parts (P) and machines (M)
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum(time_required[m][p] * machine_costs[m] * (batches[p] / 100) for m in range(M))) for p in range(P))

# Extra costs
extra_cost = pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))

# Total profit
total_profit = profit - extra_cost

# Objective
problem += total_profit, "Total_Profit"

# Constraints

# Machine time constraints
for m in range(M):
    problem += (pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) + extra_time[m] <= availability[m] + max_extra[m]), f"Machine_Availability_{m}")

# Minimum production constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p]), f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output the results
batches_result = [batches[p].varValue for p in range(P)]
extra_time_result = [extra_time[m].varValue for m in range(M)]
total_profit_value = pulp.value(problem.objective)

print(f' (Batches): {batches_result}')
print(f' (Extra Time): {extra_time_result}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')