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

A = len(data['unique_clicks'])

# Problem
problem = pulp.LpProblem("Custom_Tees_Advertising", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0) for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A))

# Constraints

# Young age clicks goal
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

# Old age clicks goal
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

# Unique young age clicks goal
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

# Unique old age clicks goal
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

# Cost budget constraint
problem += pulp.lpSum((data['costs'][a] / 1000) * x[a] for a in range(A)) <= data['budget']

# Maximum allowable clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a]

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')