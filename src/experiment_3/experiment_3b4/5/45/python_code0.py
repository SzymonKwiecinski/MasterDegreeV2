import pulp

# Data from JSON
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
A = len(data['costs'])

# Problem definition
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum([data['costs'][a] * x[a] for a in range(A)])

# Constraints
# Total clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in range(A)]) >= data['goal_young']

# Total clicks from old visitors
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in range(A)]) >= data['goal_old']

# Unique clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)]) >= data['goal_unique_young']

# Unique clicks from old visitors
problem += pulp.lpSum([data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)]) >= data['goal_unique_old']

# Maximum clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')