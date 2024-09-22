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

# Decision variables
A = range(len(data['young_clicks']))
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in A]

# Problem definition
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in A])

# Constraints
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in A]) >= data['goal_young']
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in A]) >= data['goal_old']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in A]) >= data['goal_unique_young']
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in A]) >= data['goal_unique_old']

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Extract results
result_clicks = [pulp.value(clicks[a]) for a in A]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": result_clicks,
    "total_cost": total_cost
}

# Result output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')