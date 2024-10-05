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

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Number of ad types
n_ad_types = len(data['costs'])

# Decision variables
clicks = [pulp.LpVariable(f"clicks_{i}", lowBound=0, upBound=data['max_clicks'][i], cat='Continuous') for i in range(n_ad_types)]

# Objective function
problem += pulp.lpSum([data['costs'][i] * clicks[i] for i in range(n_ad_types)])

# Constraints
problem += pulp.lpSum([data['young_clicks'][i] * clicks[i] for i in range(n_ad_types)]) >= data['goal_young'], "Young_Clicks_Goal"
problem += pulp.lpSum([data['old_clicks'][i] * clicks[i] for i in range(n_ad_types)]) >= data['goal_old'], "Old_Clicks_Goal"
problem += pulp.lpSum([data['unique_clicks'][i] * clicks[i] for i in range(n_ad_types)]) >= data['goal_unique_young'], "Unique_Young_Clicks_Goal"
problem += pulp.lpSum([data['unique_clicks'][i] * clicks[i] for i in range(n_ad_types)]) >= data['goal_unique_old'], "Unique_Old_Clicks_Goal"

# Solve the problem
problem.solve()

# Print the results
for i in range(n_ad_types):
    print(f"Clicks for ad type {i+1}: {clicks[i].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')