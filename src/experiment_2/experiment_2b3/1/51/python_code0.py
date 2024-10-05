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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Number of ad types
A = len(data['young_clicks'])

# Problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective: Maximize total unique clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)])

# Constraints

# Age group goals
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Unique click goals
problem += pulp.lpSum([data['young_clicks'][a] * data['unique_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([data['old_clicks'][a] * data['unique_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_old']

# Budget constraint
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget']

# Solve
problem.solve()

# Prepare output
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

# Print result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')