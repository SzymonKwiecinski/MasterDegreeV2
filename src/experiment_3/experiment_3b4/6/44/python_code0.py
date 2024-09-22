import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

P = len(data['prices'])
M = len(data['machine_costs'])

# Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
revenue = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
costs = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) for m in range(M)])
problem += revenue - costs

# Constraints

# Minimum Production Constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m]

# Solve the problem
problem.solve()

# Output The objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')