import pulp

# Extract data from JSON
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
A = len(data['young_clicks'])

# Problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

# Constraints
# Goal for young clicks
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']

# Goal for old clicks
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

# Goal for unique young clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']

# Goal for unique old clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

# Maximum allowable clicks
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Output results
clicks_values = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

print("Clicks purchased for each ad type:", clicks_values)
print(f"Total cost of the ad campaign: {total_cost}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')