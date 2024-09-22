import pulp

# Data from the input json
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
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision variables: number of thousands of clicks for each ad type
x = [pulp.LpVariable(f"x_{a}", lowBound=0, upBound=data['max_clicks'][a]) for a in range(len(data['costs']))]

# Objective function: Minimize total cost
problem += pulp.lpSum([data['costs'][a] * x[a] for a in range(len(data['costs']))])

# Constraint 1: Total clicks from visitors aged 18-25
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))]) >= data['goal_young']

# Constraint 2: Total clicks from visitors older than 25
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))]) >= data['goal_old']

# Constraint 3: Total unique clicks from visitors aged 18-25
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(len(data['young_clicks']))]) >= data['goal_unique_young']

# Constraint 4: Total unique clicks from visitors older than 25
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(len(data['old_clicks']))]) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')