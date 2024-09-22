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

# Create Linear Programming problem
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a+1}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

# Constraints
# 1. Clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# 2. Clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# 3. Unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']

# 4. Unique clicks from visitors older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']

# 5. Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

# 6. Maximum allowable clicks for each ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Print the results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks: {clicks_result}')
print(f'Total Unique Clicks (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')