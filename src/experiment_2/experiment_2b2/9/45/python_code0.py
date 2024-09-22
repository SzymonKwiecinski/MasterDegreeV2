import pulp

# Data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Number of ad types
A = len(data['young_clicks'])

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective function: Minimize total cost
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Constraints
# Constraint for young clicks
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_young']

# Constraint for old clicks
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_old']

# Constraint for unique clicks from young visitors
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_young']

# Constraint for unique clicks from old visitors
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_old']

# Max clicks constraints
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output results
result = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')