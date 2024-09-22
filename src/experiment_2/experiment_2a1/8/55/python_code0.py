import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Extract data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Initialize the problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) for m in range(M))
total_profit = profit - costs
problem += total_profit

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatchesConstraint_{p}"

for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * (batches[p] / 100) for p in range(P)) <= availability[m], f"AvailabilityConstraint_{m}"

# Profit constraint
problem += total_profit >= min_profit, "MinProfitConstraint"

# Solve the problem
problem.solve()

# Collect results
batches_result = [int(batches[p].varValue) for p in range(P)]
total_profit_result = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')