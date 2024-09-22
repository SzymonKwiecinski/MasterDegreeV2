import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Problem parameters
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Create the linear programming problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision variables: number of batches to produce for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize total profit
profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)])
costs = pulp.lpSum([
    (machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])) / 100 
     for m in range(M)
])
total_profit = profit - costs
problem += total_profit

# Constraints
# Minimum batches for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_{m}"

# Profit constraint
problem += total_profit >= min_profit, "MinProfit"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [int(batches[p].value()) for p in range(P)],
    "total_profit": pulp.value(total_profit)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')