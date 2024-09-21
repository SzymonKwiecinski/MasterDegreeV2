import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)])
machine_costs_total = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(M)])

problem += profit - machine_costs_total

# Constraints
# Non-negativity and minimum production constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinBatchesConstraint_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m], f"AvailabilityConstraint_{m}"

# Solve
problem.solve()

# Print results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')