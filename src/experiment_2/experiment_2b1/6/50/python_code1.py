import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'extra_costs': [0, 15, 22.5], 
        'max_extra': [0, 80, 80]}

# Extract data from the JSON-like structure
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, upBound=max_extra, cat='Continuous')

# Objective function
profit = pulp.lpSum((prices[p] * batches[p]) - 
                    pulp.lpSum((machine_costs[m] * (time_required[m][p] * batches[p] / 100 + extra_time[m])) for m in range(M)) for p in range(P))
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "extra_time": [extra_time[m].varValue for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')