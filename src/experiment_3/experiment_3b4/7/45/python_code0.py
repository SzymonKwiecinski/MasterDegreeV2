import pulp

# Data from the provided JSON
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
ad_types = len(data['costs'])

# Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(ad_types)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(ad_types))

# Constraints
# 1. Total clicks from the 18-25 age group
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_young']

# 2. Total clicks from the age group older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_old']

# 3. Total unique clicks from the 18-25 age group
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_unique_young']

# 4. Total unique clicks from the age group older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')