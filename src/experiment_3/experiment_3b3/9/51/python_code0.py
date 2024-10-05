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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Number of ad types
A = len(data['young_clicks'])

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function: Maximize total unique clicks
problem += pulp.lpSum([data['unique_clicks'][a] * x[a] for a in range(A)])

# Constraints
# Target clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in range(A)]) >= data['goal_young']

# Target clicks from old visitors
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in range(A)]) >= data['goal_old']

# Target unique clicks from young visitors
problem += pulp.lpSum([data['unique_clicks'][a] * x[a] for a in range(A)]) >= data['goal_unique_young']

# Target unique clicks from old visitors
problem += pulp.lpSum([data['unique_clicks'][a] * x[a] for a in range(A)]) >= data['goal_unique_old']

# Budget constraint
problem += pulp.lpSum([data['costs'][a] * x[a] for a in range(A)]) <= data['budget']

# Solve the problem
problem.solve()

# Print the results
clicks = [pulp.value(x[a]) for a in range(A)]
total_unique_clicks = sum([data['unique_clicks'][a] * clicks[a] for a in range(A)])
print("Clicks purchased for each ad type (in thousands):", clicks)
print("Total unique clicks:", total_unique_clicks)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')