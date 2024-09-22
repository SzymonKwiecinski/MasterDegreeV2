import pulp
import json

# Data from JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}")

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra", range(M), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + extra_time[m]) for m in range(M)]) - \
         pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(M)])

problem += profit, "Total_Profit"

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= (availability[m] + extra_time[m])), f"Machine_Availability_{m}"

# Minimum Production Requirement
for p in range(P):
    problem += (batches[p] >= min_batches[p]), f"Min_Production_{p}"

# Extra Time Limit
for m in range(M):
    problem += (extra_time[m] <= max_extra[m]), f"Extra_Time_Limit_{m}"

# Solve the problem
problem.solve()

# Print the results
batches_solution = [batches[p].varValue for p in range(P)]
extra_time_solution = [extra_time[m].varValue for m in range(M)]
print(f'Batches produced: {batches_solution}')
print(f'Extra time purchased: {extra_time_solution}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')