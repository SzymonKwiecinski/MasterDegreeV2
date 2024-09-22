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

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['max_clicks'][i], cat='Continuous') for i in range(len(data['young_clicks']))]

# Problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(len(x))), "Total Unique Clicks"

# Constraints
# Click constraint for young visitors
problem += pulp.lpSum(data['young_clicks'][i] * x[i] for i in range(len(x))) >= data['goal_young'], "Goal Young Clicks"

# Click constraint for old visitors
problem += pulp.lpSum(data['old_clicks'][i] * x[i] for i in range(len(x))) >= data['goal_old'], "Goal Old Clicks"

# Unique click constraint for young visitors
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(len(x))) >= data['goal_unique_young'], "Goal Unique Young Clicks"

# Unique click constraint for old visitors
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(len(x))) >= data['goal_unique_old'], "Goal Unique Old Clicks"

# Budget constraint
problem += pulp.lpSum(data['costs'][i] * x[i] for i in range(len(x))) <= data['budget'], "Budget Constraint"

# Solve the problem
problem.solve()

# Output results
clicks = [pulp.value(x[i]) for i in range(len(x))]
print(f'Optimal clicks distribution: {clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')