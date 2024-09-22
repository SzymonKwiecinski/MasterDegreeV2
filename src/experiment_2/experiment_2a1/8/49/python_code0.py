import pulp
import json

# Input data in json format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extract data from the input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define parameters
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables: batches of each part produced
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Total profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] / 100 for p in range(P)]) for m in range(M)])

problem += profit, "Total_Profit"

# Constraints for batches produced
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_{m}"

# Additional constraint for sharing availability of Machine M and M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2], "Shared_Availability"

# Solve the problem
problem.solve()

# Prepare the output
batches_output = [int(batches[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print the result
output = {"batches": batches_output, "total_profit": total_profit}
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')