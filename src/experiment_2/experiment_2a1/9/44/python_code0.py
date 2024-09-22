import json
import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting data from the input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
P = len(prices)
M = len(machine_costs)

problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit_expr = pulp.lpSum((prices[p] * batches[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100) * batches[p] for m in range(M))) for p in range(P))
problem += profit_expr, "Total_Profit"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Collecting results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')