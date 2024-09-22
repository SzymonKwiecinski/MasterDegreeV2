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

# Problem Setup
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("ExtraTime", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum((data['prices'][p] * batches[p]) for p in range(P)) - \
         pulp.lpSum((data['machine_costs'][m] * 
                      (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)))) + 
                     extra_time[m] * data['extra_costs'][m] for m in range(M))
problem += profit

# Constraints
# Min batches constraint
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine availability constraint
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m] <= data['availability'][m] + data['max_extra'][m])

# Solve the problem
problem.solve()

# Collecting results
batches_result = [int(batches[p].varValue) for p in range(P)]
extra_time_result = [int(extra_time[m].varValue) for m in range(M)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')