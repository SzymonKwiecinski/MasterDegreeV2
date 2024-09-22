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

# Unpack data
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

# Number of ad types
A = len(costs)

# Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum([costs[a] * x[a] for a in range(A)])

# Constraints

# Clicks from visitors aged 18-25
problem += pulp.lpSum([young_clicks[a] * x[a] for a in range(A)]) >= goal_young

# Clicks from visitors older than 25
problem += pulp.lpSum([old_clicks[a] * x[a] for a in range(A)]) >= goal_old

# Unique clicks from visitors aged 18-25
problem += pulp.lpSum([young_clicks[a] * unique_clicks[a] * x[a] for a in range(A)]) >= goal_unique_young

# Unique clicks from visitors older than 25
problem += pulp.lpSum([old_clicks[a] * unique_clicks[a] * x[a] for a in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')