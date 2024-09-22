import pulp
import json

# Parse the provided JSON data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Extract data from the parsed JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define the number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0)

# Define the objective function
problem += pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
            pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

# Define the constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m+1}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p+1}"

# Solve the problem
problem.solve()

# Output the results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
print(f' Batches produced for each part: {batches_solution}')