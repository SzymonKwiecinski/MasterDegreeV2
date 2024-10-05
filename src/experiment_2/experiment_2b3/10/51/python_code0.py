import pulp

# Data from JSON
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

# Decision Variable
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{i}', lowBound=0, upBound=data['max_clicks'][i], cat='Continuous') for i in range(A)]

# Problem Definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Objective Function: Maximize unique clicks
problem += pulp.lpSum([clicks[i] * data['unique_clicks'][i] for i in range(A)])

# Constraints
# Budget Constraint
problem += pulp.lpSum([clicks[i] * data['costs'][i] for i in range(A)]) <= data['budget']

# Age group goals
problem += pulp.lpSum([clicks[i] * data['young_clicks'][i] for i in range(A)]) >= data['goal_young']
problem += pulp.lpSum([clicks[i] * data['old_clicks'][i] for i in range(A)]) >= data['goal_old']

# Unique age group goals
problem += pulp.lpSum([clicks[i] * data['unique_clicks'][i] * (data['young_clicks'][i] / 100) for i in range(A)]) >= data['goal_unique_young']
problem += pulp.lpSum([clicks[i] * data['unique_clicks'][i] * (data['old_clicks'][i] / 100) for i in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Solution
click_values = [pulp.value(clicks[i]) for i in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": click_values,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')