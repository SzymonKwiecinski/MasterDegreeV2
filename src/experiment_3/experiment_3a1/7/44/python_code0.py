import pulp
import json

# Data provided in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extract the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Define the decision variables
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - pulp.lpSum(
    [machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]
)
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Production_{p}"

# Solve the problem
problem.solve()

# Print the results
batches_produced = [batches[p].varValue for p in range(P)]
print(f'Batches Produced: {batches_produced}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')