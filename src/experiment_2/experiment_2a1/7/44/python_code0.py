import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Problem parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)    # Number of different parts
M = len(machine_costs)  # Number of different machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
total_profit = pulp.lpSum((prices[p] * batches[p] for p in range(P))) - \
               pulp.lpSum((machine_costs[m] * pulp.lpSum((time_required[m][p] / 100) * batches[p] for p in range(P)) for m in range(M)))

problem += total_profit

# Constraints
# Machine time availability constraints
for m in range(M):
    problem += (pulp.lpSum((time_required[m][p] / 100) * batches[p] for p in range(P)) <= availability[m])

# Minimum batches constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p])

# Solve the problem
problem.solve()

# Output results
batches_result = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)
result = {
    "batches": batches_result,
    "total_profit": total_profit_value
}

# Printing the result
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')