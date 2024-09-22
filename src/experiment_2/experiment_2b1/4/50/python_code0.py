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

# Problem parameters
M = len(data['availability'])
P = len(data['prices'])

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Objective Function
profit = pulp.lpSum((data['prices'][p] * batches[p] for p in range(P))) - \
         pulp.lpSum((data['machine_costs'][m] * (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) / 100) 
                      + data['extra_costs'][m] * extra_time[m]) for m in range(M))

problem += profit

# Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"MinBatches_{p}"

for m in range(M):
    total_time = pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + extra_time[m]
    problem += total_time <= data['availability'][m] + data['max_extra'][m], f"MachineAvailability_{m}"

# Solve problem
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

print(output)