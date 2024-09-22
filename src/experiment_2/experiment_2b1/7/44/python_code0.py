import pulp
import json

# Input data in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting data from the JSON-like structure
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum(
    [machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] / 100 for p in range(P)]) for m in range(M)]
)

problem += profit

# Constraints for machine availability
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}")

# Constraints for minimum batches
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Batches_{p}")

# Solve the problem
problem.solve()

# Output results
produced_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

result = {
    "batches": produced_batches,
    "total_profit": total_profit
}

# Print the result
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')