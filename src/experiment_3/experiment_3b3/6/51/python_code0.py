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
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective function
total_unique_clicks = pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))
problem += total_unique_clicks

# Constraints
# Goal of clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

# Goal of clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

# Goal of unique clicks
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= (data['goal_unique_young'] + data['goal_unique_old'])

# Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

# Maximum allowable clicks for each ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output the results
results = [pulp.value(clicks[a]) for a in range(A)]
print(f'Clicks purchased for each ad type: {results}')
print(f'Total unique clicks (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')