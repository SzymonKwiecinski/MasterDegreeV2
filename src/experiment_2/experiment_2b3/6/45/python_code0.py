import pulp

# Problem data from the JSON input
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

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables: number of clicks to purchase for each ad type
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Minimize total cost
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A))

# Constraints
# Goal of young clicks
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# Goal of old clicks
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# Goal of unique young clicks
problem += pulp.lpSum(data['unique_clicks'][a] * 0.01 * data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']

# Goal of unique old clicks
problem += pulp.lpSum(data['unique_clicks'][a] * 0.01 * data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

# Output the results in the required format
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')