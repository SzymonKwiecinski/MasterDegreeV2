import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extract data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: batches of each part produced
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
costs = pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P)) for m in range(M))
problem += profit - costs

# Constraints
# Min batches constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Availability constraints
total_time = pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(P) for m in range(M))
availability_constraint = pulp.lpSum(total_time) <= sum(availability)  # Machines M and M-1 can share
problem += availability_constraint, "Total_Availability"

# Solve the problem
problem.solve()

# Prepare output
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')