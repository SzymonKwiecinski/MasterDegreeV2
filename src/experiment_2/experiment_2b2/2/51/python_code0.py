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

# Define problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables: number of clicks purchased for each ad type
num_ads = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(num_ads)]

# Objective: Maximize the total number of unique clicks
total_unique_clicks = pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(num_ads)])
problem += total_unique_clicks, "Total Unique Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum([clicks[a] * data['costs'][a] for a in range(num_ads)]) <= data['budget'], "Budget"

# Young clicks goal
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(num_ads)]) >= data['goal_young'], "Goal Young"

# Old clicks goal
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(num_ads)]) >= data['goal_old'], "Goal Old"

# Unique young clicks goal
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(num_ads)]) >= data['goal_unique_young'], "Goal Unique Young"

# Unique old clicks goal
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] * data['unique_clicks'][a] / 100 for a in range(num_ads)]) >= data['goal_unique_old'], "Goal Unique Old"

# Solve the problem
problem.solve()

# Results
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(num_ads)],
    "total_unique_clicks": pulp.value(total_unique_clicks)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')