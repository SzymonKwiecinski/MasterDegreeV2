import pulp
import json

# Data in JSON format
data_json = '''
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10], 
    "extra_costs": [0, 15, 22.5], 
    "max_extra": [0, 80, 80]
}
'''
data = json.loads(data_json)

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the model
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # b_p
extra_hours = pulp.LpVariable.dicts("e", range(M), lowBound=0)  # e_m

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
cost = pulp.lpSum(data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_hours[m]) for m in range(M))
extra_cost = pulp.lpSum(data['extra_costs'][m] * extra_hours[m] for m in range(M))
problem += profit - cost - extra_cost

# Constraints
# Production Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine Time Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required[m][p] * batches[p] for p in range(P)]) + extra_hours[m] <= data['availability'][m] + data['max_extra'][m]

# Solve the problem
problem.solve()

# Output the results
batches_solution = [batches[p].varValue for p in range(P)]
extra_time_solution = [extra_hours[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches_solution}')
print(f' (Extra Hours Purchased): {extra_time_solution}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')