import pulp

# Problem data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Number of ad types
A = len(data['young_clicks'])

# Create LP problem with corrected name
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective function: Maximize total unique clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)])

# Constraints
# Budget constraint
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(A)]) <= data['budget']

# Young clicks goal
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(A)]) >= data['goal_young']

# Old clicks goal
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(A)]) >= data['goal_old']

# Unique young clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] * data['young_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_young']

# Unique old clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] * data['old_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_old']

# Max clicks constraint for each ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Prepare the result
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output format
result = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')