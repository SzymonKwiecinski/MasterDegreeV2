import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Indices
P = len(data['prices'])
M = len(data['machine_costs'])

# Parameters
time_required = data['time_required']
cost = data['machine_costs']
availability = data['availability']
price = data['prices']
min_batches = data['min_batches']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

# Objective Function
problem += (
    pulp.lpSum([price[p] * x[p] for p in range(P)]) 
    - pulp.lpSum([cost[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) for m in range(M)])
)

# Constraints
# Time availability constraints for machines 1 to M-2
for m in range(M - 2):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m]

# Combined availability constraint for machine M-1 and machine M
problem += pulp.lpSum([time_required[M-1][p] * x[p] + time_required[M][p] * x[p] for p in range(P)]) <= availability[M-1] + availability[M]

# Minimum production requirement for each part
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')