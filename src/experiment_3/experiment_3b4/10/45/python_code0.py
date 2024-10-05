import pulp

# Data from the JSON
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

# Problem definition
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A))

# Constraints
# 1. Total clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# 2. Total clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# 3. Total unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# 4. Total unique clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')