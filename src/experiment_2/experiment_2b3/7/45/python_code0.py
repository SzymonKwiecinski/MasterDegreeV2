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

A = len(data['young_clicks'])

# LP Problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a-1], cat='Continuous') for a in range(1, A+1)]

# Objective Function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)]), "Total_Cost"

# Constraints
# Goal on young clicks
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young'] * 10

# Goal on old clicks
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old'] * 10

# Goal on unique young clicks
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_young'] * 10

# Goal on unique old clicks
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] / 100 for a in range(A)]) >= data['goal_unique_old'] * 10

# Solve the problem
problem.solve()

# Output results
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')