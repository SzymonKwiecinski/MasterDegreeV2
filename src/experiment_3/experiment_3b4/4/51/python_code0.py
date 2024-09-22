import pulp

# Data from the JSON format
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
A = len(data['costs'])

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

# Problem definition
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)), "Total Unique Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "Budget"

# Goal for young age group
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Goal_Young"

# Goal for old age group
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Goal_Old"

# Goal for unique clicks for young (18-25)
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

# Goal for unique clicks for old (above 25)
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for a in range(A):
    print(f'Clicks for Ad Type {a+1}: {clicks[a].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')