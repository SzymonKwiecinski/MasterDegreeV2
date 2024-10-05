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

# Problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Indices
num_ads = len(data['costs'])
ads = range(num_ads)

# Decision Variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in ads]

# Objective Function
problem += pulp.lpSum([data['costs'][a] * x[a] for a in ads]), "Total Cost"

# Constraints
# Young age clicks constraint
problem += pulp.lpSum([data['young_clicks'][a] * x[a] for a in ads]) >= data['goal_young'], "Young_Age_Clicks"

# Older age clicks constraint
problem += pulp.lpSum([data['old_clicks'][a] * x[a] for a in ads]) >= data['goal_old'], "Old_Age_Clicks"

# Unique young clicks constraint
problem += pulp.lpSum([data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in ads]) >= data['goal_unique_young'], "Unique_Young_Clicks"

# Unique old clicks constraint
problem += pulp.lpSum([data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in ads]) >= data['goal_unique_old'], "Unique_Old_Clicks"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')