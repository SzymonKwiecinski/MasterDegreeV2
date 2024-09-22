import pulp
import json

# Input Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Extracting Data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("Extra_Time", range(M), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum(time_required[m][p] * batches[p] * machine_costs[m] for m in range(M)) -
                     pulp.lpSum(extra_time[m] * extra_costs[m] for m in range(M)) ) for p in range(P))

problem += profit

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]  # Minimum batches
    for m in range(M):
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
                     extra_time[m]) <= availability[m] + max_extra[m]  # Machine availability 

# Solve the problem
problem.solve()

# Output Results
batches_result = [batches[p].varValue for p in range(P)]
extra_time_result = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

output = {
    "batches": batches_result,
    "extra_time": extra_time_result,
    "total_profit": total_profit
}

print(output)