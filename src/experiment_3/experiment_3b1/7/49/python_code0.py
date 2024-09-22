import pulp
import json

# Given data in JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extracting parameters from the JSON data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the model
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Define indices
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) \
         - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total Profit"

# Constraints
# Machine availability constraints for each machine except the last two sharing availability
for m in range(M-1):  # considering M and M-1 can share
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Constraint_Machine_{m+1}"

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum_Batches_Constraint_Part_{p+1}"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')