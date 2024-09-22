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

# Number of ad types
A = len(data['young_clicks'])

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A))

# Constraints
# 1. Clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# 2. Clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# 3. Unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# 4. Unique clicks from visitors older than 25
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * x[a] for a in range(A)) >= data['goal_unique_old']

# 5. Maximum allowable clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')