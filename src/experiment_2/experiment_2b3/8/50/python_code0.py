import pulp

# Define the data from the JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Extracting the variables from the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Number of parts and machines
P = len(prices)
M = len(availability)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P))
machine_costs_total = pulp.lpSum((machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P))) for m in range(M))
extra_costs_total = pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))
problem += profit - machine_costs_total - extra_costs_total

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m]

# Solve the problem
problem.solve()

# Extract the results
output = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "extra_time": [extra_time[m].varValue for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')