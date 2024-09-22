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

A = len(data['costs'])

# Create a LP Minimization problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0) for a in range(A)]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A))

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Clicks_Young_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Clicks_Old_Constraint"

for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_Constraint_{a}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')