import pulp
import json

# Input Data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: batches of each part
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')

# Objective function: maximize total profit
total_revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
total_cost = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] / 100 * batches[p] for p in range(P)) for m in range(M))
problem += total_revenue - total_cost

# Constraints: machine availability and minimum batches
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] / 100 * batches[p] for p in range(P)) <= availability[m]

for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')