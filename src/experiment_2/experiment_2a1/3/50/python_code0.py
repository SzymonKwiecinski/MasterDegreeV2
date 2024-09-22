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

# Problem variables
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function coefficients
profit = sum((data['prices'][p] * batches[p]) for p in range(P))
costs = sum((data['machine_costs'][m] * 
              sum(data['time_required'][m][p] * batches[p] for p in range(P)) / 100) for m in range(M))
extra_costs = sum(data['extra_costs'][m] * extra_time[m] for m in range(M))

# Objective function
problem += profit - costs - extra_costs

# Constraints for minimum production
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Constraints for machine time
for m in range(M):
    problem += (sum(data['time_required'][m][p] * batches[p] for p in range(P)) / 100 +
                 extra_time[m] <= data['availability'][m] + data['max_extra'][m])

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
extra_time_result = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

# Print results
print(json.dumps({
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit
}))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')