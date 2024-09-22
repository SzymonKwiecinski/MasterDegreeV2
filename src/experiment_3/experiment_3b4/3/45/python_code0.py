import pulp

# Data provided in JSON format
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

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A))

# Constraints
# 1. Goal for clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# 2. Goal for clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# 3. Goal for unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']

# 4. Goal for unique clicks from visitors older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Display individual decision variable values
for a in range(A):
    print(f'Clicks for ad type {a + 1}: {clicks[a].varValue}')