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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Indices
A = len(data['young_clicks'])

# Create the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total Unique Clicks"

# Constraints
# Budget constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget Constraint"

# Goal for young clicks
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal for Young Clicks"

# Goal for old clicks
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal for Old Clicks"

# Goal for unique young clicks
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal for Unique Young Clicks"

# Goal for unique old clicks
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal for Unique Old Clicks"

# Maximum clicks per ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max Clicks for Ad {a+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')