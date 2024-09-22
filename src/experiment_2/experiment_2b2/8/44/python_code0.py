import pulp

# Input data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10]
}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(time_required)  # number of machines
P = len(time_required[0])  # number of parts

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function
total_profit = pulp.lpSum([batches[p] * (prices[p] 
                 - sum(time_required[m][p] * machine_costs[m] for m in range(M))) for p in range(P)])

problem += total_profit

# Constraints
# Machine time constraints
for m in range(M):
    problem += pulp.lpSum([batches[p] * time_required[m][p] for p in range(P)]) <= availability[m]

# Solve
problem.solve()

# Output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')