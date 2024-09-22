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
A = len(data['young_clicks'])

# Problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0, cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A))

# Constraints
# Young clicks constraint
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# Old clicks constraint
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# Unique young clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# Unique old clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

# Maximum allowable clicks constraint
for a in range(A):
    problem += x[a] <= data['max_clicks'][a]

# Solve
problem.solve()

# Print the results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
for a in range(A):
    print(f"x_{a+1} = {x[a].varValue} thousand clicks")