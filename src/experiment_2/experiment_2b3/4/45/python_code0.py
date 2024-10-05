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

# Initialize the problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision variables: Number of clicks in thousands for each ad type
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

# Objective: Minimize the total cost of clicks
total_cost = pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])
problem += total_cost

# Constraints
# 1. Total clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_young']

# 2. Total clicks from older visitors
problem += pulp.lpSum([data['old_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_old']

# 3. Total unique clicks from young visitors
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)
                       if data['young_clicks'][a] / 100 * clicks[a] >= data['goal_unique_young']]) >= data['goal_unique_young']

# 4. Total unique clicks from older visitors
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)
                       if data['old_clicks'][a] / 100 * clicks[a] >= data['goal_unique_old']]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(total_cost)
}

# Print the solution
print(f'Solution: {solution}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')