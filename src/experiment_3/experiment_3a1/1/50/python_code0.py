import pulp
import json

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

# Parameters from the data
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0)  # b_p
extra_hours = pulp.LpVariable.dicts("ExtraHours", range(M), lowBound=0)  # extra_m

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) 
costs = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_hours[m]) for m in range(M))
extra_cost = pulp.lpSum(data['extra_costs'][m] * extra_hours[m] for m in range(M))

problem += profit - costs - extra_cost, "Total_Profit"

# Constraints
# Machine Time Constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required[m][p]'] * batches[p] for p in range(P)) + extra_hours[m] <= data['availability'][m] + data['max_extra'][m]), f"Time_Constraint_Machine_{m}"

# Minimum Production Requirement
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p]), f"Min_Production_Requirement_Part_{p}"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Batches produced for part {p}: {batches[p].varValue}')

for m in range(M):
    print(f'Extra hours purchased for machine {m}: {extra_hours[m].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')