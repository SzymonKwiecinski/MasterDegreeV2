import pulp

# Input data
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

# Variables
A = len(data['young_clicks'])
clicks = pulp.LpVariable.dicts("Clicks", range(A), 0)

# Problem
problem = pulp.LpProblem("Maximize Unique Clicks", pulp.LpMaximize)

# Objective
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]), "Total Unique Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]) <= data['budget'], "Budget"

# Clicks constraints
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a], f"Max Clicks {a}"

# Young clicks constraint
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young'], "Young Clicks"

# Old clicks constraint
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old'], "Old Clicks"

# Unique young clicks constraint
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_young'], "Unique Young Clicks"

# Unique old clicks constraint
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_old'], "Unique Old Clicks"

# Solve
problem.solve()

# Results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')