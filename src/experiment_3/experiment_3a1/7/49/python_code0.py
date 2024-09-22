import pulp
import json

# Given data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraint
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Minimum batch production constraint
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum_Batch_Production_{p}"

# Shared availability condition
if M > 1:  # Ensure there are at least two machines
    problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + \
               pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1], "Shared_Availability"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Number of batches for part {p}: {batches[p].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')