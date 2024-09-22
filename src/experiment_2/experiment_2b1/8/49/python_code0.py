import pulp
import json

# Input Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * machine_costs[m] / 100) * batches[p] 
                                 for m in range(M))) 
                     for p in range(P))
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Gather results
result_batches = [batches[p].value() for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')