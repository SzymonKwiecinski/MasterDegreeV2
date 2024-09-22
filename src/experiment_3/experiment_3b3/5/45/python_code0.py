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

# Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total Cost"

# Constraints
# Total clicks from young visitors
problem += pulp.lpSum(data['young_clicks'][a] / 100 * x[a] for a in range(A)) >= data['goal_young'], "Goal Young Clicks"

# Total clicks from older visitors
problem += pulp.lpSum(data['old_clicks'][a] / 100 * x[a] for a in range(A)) >= data['goal_old'], "Goal Old Clicks"

# Total unique clicks from young visitors
problem += pulp.lpSum(data['unique_clicks'][a] / 100 * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal Unique Young Clicks"

# Total unique clicks from older visitors
problem += pulp.lpSum(data['unique_clicks'][a] / 100 * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal Unique Old Clicks"

# Maximum allowable clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max Clicks {a}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')