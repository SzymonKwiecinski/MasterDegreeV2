import pulp
import json

# Data input
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extracting data from the JSON
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

# Create decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit_expr = pulp.lpSum([
    prices[p] * batches[p] - 
    pulp.lpSum([machine_costs[m] * time_required[m][p] * batches[p] for m in range(M)])
    for p in range(P)
])
problem += profit_expr, "Total_Profit"

# Constraints
# Machine Time Availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_Machine_{m+1}"

# Minimum Production Requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Requirement_Part_{p+1}"

# Solve the problem
problem.solve()

# Output results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')