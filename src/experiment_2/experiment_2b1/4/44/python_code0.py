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

# Define parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_for_Part_{p}"

for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_for_Machine_{m}"

# Solve the problem
problem.solve()

# Prepare the output
output_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print the result
result = {
    "batches": output_batches,
    "total_profit": total_profit
}

print(result)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')