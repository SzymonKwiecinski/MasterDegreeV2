import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting values
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Problem definition
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Integer') for p in range(P)]

# Objective function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(P))
machine_cost = pulp.lpSum(
    pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) * machine_costs[m] for m in range(M)
)
problem += revenue - machine_cost

# Constraints
# Machine availability constraint
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Combined availability for machines M and M-1
problem += (pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) +
            pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P)) <= 
            availability[M-1] + availability[M-2])

# Solving the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')