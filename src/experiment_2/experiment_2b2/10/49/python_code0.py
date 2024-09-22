import pulp

# Data from the JSON input
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: maximize profit
profit = sum((prices[p] - sum(time_required[m][p] * machine_costs[m] for m in range(M))) * batches[p] for p in range(P))
problem += profit

# Constraints: machine hour availability 
# Machine M and Machine M-1 share availability
for m in range(M-2):
    problem += sum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]
problem += sum(sum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M-2, M)) <= availability[M-1]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')