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

# Problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

# Constraints
# (1) Target clicks from 18-25 age group
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# (2) Target clicks from older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# (3) Target unique clicks
total_unique_goals = data['goal_unique_young'] + data['goal_unique_old']
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= total_unique_goals

# (4) Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

# (5) Max clicks per ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')