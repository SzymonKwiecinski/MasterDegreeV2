import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['time_required'])  # Number of machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0)

# Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)), "Total_Profit"

# Constraints
# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Availability_Constraint_{m}"

# Minimum production requirement
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')