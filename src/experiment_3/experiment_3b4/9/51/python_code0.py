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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A))

# Constraints
# Total clicks for visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# Total clicks for visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# Total unique clicks for visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# Total unique clicks for visitors older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

# Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')