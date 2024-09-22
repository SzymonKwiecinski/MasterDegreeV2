import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

P = len(data['prices'])
M = len(data['machine_costs'])

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['time_required'][m][p] * batches[p] * data['machine_costs'][m] for m in range(M)) for p in range(P)))
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m]

# Constraints for extra time costs
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Extract results
batches_result = [batches[p].varValue for p in range(P)]
extra_time_result = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')