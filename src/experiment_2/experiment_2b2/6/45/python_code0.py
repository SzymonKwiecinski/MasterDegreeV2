import pulp

# Parsing the input data
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

# Number of ad types
A = len(data['young_clicks'])

# Problem definition
problem = pulp.LpProblem("Minimize_Ad_Campaign_Cost", pulp.LpMinimize)

# Decision variables: Number of clicks from each ad type in thousands
clicks = [pulp.LpVariable(f'clicks_{i}', lowBound=0, cat='Continuous') for i in range(A)]

# Objective function: Minimize total cost
problem += pulp.lpSum([data['costs'][i] * clicks[i] for i in range(A)])

# Constraint 1: Total young clicks
problem += pulp.lpSum([data['young_clicks'][i] / 100 * clicks[i] for i in range(A)]) >= data['goal_young']

# Constraint 2: Total old clicks
problem += pulp.lpSum([data['old_clicks'][i] / 100 * clicks[i] for i in range(A)]) >= data['goal_old']

# Constraint 3: Total unique young clicks
problem += pulp.lpSum([data['unique_clicks'][i] / 100 * clicks[i] for i in range(A)]) >= data['goal_unique_young']

# Constraint 4: Total unique old clicks
problem += pulp.lpSum([data['unique_clicks'][i] / 100 * clicks[i] for i in range(A)]) >= data['goal_unique_old']

# Constraints 5: Maximum click limits per ad type
for i in range(A):
    problem += clicks[i] <= data['max_clicks'][i]

# Solve the problem
problem.solve()

# Extract the results
clicks_result = [pulp.value(clicks[i]) for i in range(A)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')