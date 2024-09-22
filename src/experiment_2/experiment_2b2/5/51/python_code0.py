import pulp

# Load data
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

# Problem definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables: number of clicks for each ad type in thousands
clicks = [pulp.LpVariable(f'click_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: maximize unique clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)])

# Constraints
# Budget constraint
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget']

# Clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']

# Clicks from old visitors
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Unique clicks constraint for young visitors
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_young']

# Unique clicks constraint for old visitors
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Output the results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')