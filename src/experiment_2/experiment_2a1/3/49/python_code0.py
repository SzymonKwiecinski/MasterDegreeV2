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

# Extracting data from JSON-like input
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost_m
availability = data['availability']      # available_m
prices = data['prices']                  # price_p
min_batches = data['min_batches']        # min_batches_p

# Number of machines (M) and parts (P)
M = len(machine_costs)
P = len(prices)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize total profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] / 100 for m in range(M))) for p in range(P))
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Solve the problem
problem.solve()

# Result extraction
batches_result = [int(batches[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

# Print result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')