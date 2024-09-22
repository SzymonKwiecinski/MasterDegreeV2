import pulp

# Data from the JSON
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

# Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Constraints
# Young age group clicks
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']

# Old age group clicks
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Unique young clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']

# Unique old clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Output the solution
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

print("Clicks per ad type:")
for a in range(A):
    print(f"Ad Type {a + 1}: {clicks_result[a]:.2f} thousand clicks")
print(f"Total Cost: {total_cost:.2f}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')