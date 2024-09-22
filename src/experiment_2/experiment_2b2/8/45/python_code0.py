import pulp

# Problem Data
data = {
    "goal_young": 500,
    "goal_old": 600,
    "goal_unique_young": 250,
    "goal_unique_old": 300,
    "young_clicks": [40, 30, 70],
    "old_clicks": [60, 70, 30],
    "costs": [75, 100, 120],
    "max_clicks": [600, 300, 300],
    "unique_clicks": [40, 75, 90]
}

# Problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Variables
clicks = [pulp.LpVariable(f"clicks_{a}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(len(data['costs']))]

# Objective
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(len(data['costs']))]), "Total Cost"

# Constraints
# Goal for young clicks
problem += pulp.lpSum([clicks[a] * data['young_clicks'][a] for a in range(len(clicks))]) >= data['goal_young'], "Goal Young"

# Goal for old clicks
problem += pulp.lpSum([clicks[a] * data['old_clicks'][a] for a in range(len(clicks))]) >= data['goal_old'], "Goal Old"

# Unique goal for young clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(len(clicks))]) >= data['goal_unique_young'], "Unique Goal Young"

# Unique goal for old clicks
problem += pulp.lpSum([clicks[a] * data['unique_clicks'][a] for a in range(len(clicks))]) >= data['goal_unique_old'], "Unique Goal Old"

# Solve
problem.solve()

# Output
output = {
    "clicks": [pulp.value(clicks[a]) for a in range(len(clicks))],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')