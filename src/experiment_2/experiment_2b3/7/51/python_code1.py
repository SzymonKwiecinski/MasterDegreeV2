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

# Number of ad types
A = len(data['young_clicks'])

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

# Objective: Maximize total unique clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(A)]), "Total_Unique_Clicks"

# Constraints
# 1. Total budget constraint
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(A)]) <= data['budget'], "Budget_Constraint"

# 2. Goal for young clicks
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(A)]) >= data['goal_young'] * 1000, "Goal_Young_Clicks"

# 3. Goal for old clicks
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(A)]) >= data['goal_old'] * 1000, "Goal_Old_Clicks"

# 4. Goal for unique young clicks
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_young'] * 1000, "Goal_Unique_Young_Clicks"

# 5. Goal for unique old clicks
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(A)]) >= data['goal_unique_old'] * 1000, "Goal_Unique_Old_Clicks"

# Solve the problem
problem.solve()

# Output the results
solution = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_unique_clicks": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')