import pulp

# Data input
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

# Create the LP problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Minimize total cost
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Constraints
# Young clicks goal
problem += pulp.lpSum([data['young_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_young']

# Old clicks goal
problem += pulp.lpSum([data['old_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_old']

# Unique young clicks goal
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_young']

# Unique old clicks goal
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Output solution
clicks_solution = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": clicks_solution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')