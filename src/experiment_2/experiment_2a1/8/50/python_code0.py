import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
profit = sum((prices[p] * batches[p] - 
              sum(time_required[m][p] * machine_costs[m] * (batches[p] / 100) for m in range(M)))
             for p in range(P))
total_extra_cost = sum(extra_time[m] * extra_costs[m] for m in range(M))
problem += profit - total_extra_cost

# Constraints
# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Machine availability constraints
for m in range(M):
    problem += (sum(time_required[m][p] * (batches[p] / 100) for p in range(P)) +
                 extra_time[m]) <= availability[m] + max_extra[m]

# Solve the problem
problem.solve()

# Output results
batches_solution = [int(batches[p].varValue) for p in range(P)]
extra_time_solution = [extra_time[m].varValue for m in range(M)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_solution,
    "extra_time": extra_time_solution,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')