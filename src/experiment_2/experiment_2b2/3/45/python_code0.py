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
A = len(costs)

# Define the Linear Programming problem
problem = pulp.LpProblem('Minimize_Ad_Cost', pulp.LpMinimize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints

# Young age group clicks
problem += pulp.lpSum([young_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_young

# Old age group clicks
problem += pulp.lpSum([old_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_old

# Unique young clicks 
problem += pulp.lpSum([unique_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_unique_young

# Unique old clicks
problem += pulp.lpSum([unique_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Prepare the output
output = {
    'clicks': [pulp.value(clicks[a]) for a in range(A)],
    'total_cost': pulp.value(problem.objective)
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')