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
    'unique_clicks': [40, 75, 90]
}

# Extract data
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
A = len(young_clicks)

# Define the LP problem
problem = pulp.LpProblem("CustomTeesAdCampaign", pulp.LpMinimize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', 0, max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints
# Total clicks from young visitors
problem += pulp.lpSum([young_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_young

# Total clicks from old visitors
problem += pulp.lpSum([old_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_old

# Total unique clicks from young visitors
problem += pulp.lpSum([unique_clicks[a] / 100 * young_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_unique_young

# Total unique clicks from old visitors
problem += pulp.lpSum([unique_clicks[a] / 100 * old_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Prepare the results
results = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(problem.objective)
}

# Print the results
print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')