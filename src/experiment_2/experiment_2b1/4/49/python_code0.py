import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extract data from the JSON format
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
P = len(prices)  # Number of products
M = len(machine_costs)  # Number of machines

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[p] - pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] / 100 for m in range(M))) * batches[p] for p in range(P))
problem += profit

# Constraints for minimum batches
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Solve the problem
problem.solve()

# Output results
results = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')