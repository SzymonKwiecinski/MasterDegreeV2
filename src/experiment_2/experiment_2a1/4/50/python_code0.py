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

# Variables
P = len(data['prices'])
M = len(data['machine_costs'])

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum((data['time_required[m][p] * data["machine_costs"][m]" for m in range(M)]) * batches[p]) -
                     (extra_time[m] * data['extra_costs'][m] for m in range(M) if extra_time[m] > 0)) for p in range(P))

problem += profit

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m]

# Solve the problem
problem.solve()

# Output results
batches_solution = [batches[p].varValue for p in range(P)]
extra_time_solution = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
output = {
    "batches": batches_solution,
    "extra_time": extra_time_solution,
    "total_profit": total_profit
}