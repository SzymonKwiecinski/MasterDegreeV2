import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting information from data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of machines and parts
M = len(machine_costs)
P = len(prices)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function: Total profit
total_profit = pulp.lpSum((prices[p] * batches[p] for p in range(P))) - \
               pulp.lpSum((machine_costs[m] * pulp.lpSum((time_required[m][p] * batches[p] for p in range(P))) / 100 for m in range(M)))

problem += total_profit, "Total_Profit"

# Constraints
# Minimum batches for each part
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Batch_{p}")

# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum((time_required[m][p] * batches[p] for p in range(P))) <= availability[m], f"Availability_{m}")

# Solve the problem
problem.solve()

# Output the results
batches_result = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit_value
}

# JSON output
print(json.dumps(output))

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')