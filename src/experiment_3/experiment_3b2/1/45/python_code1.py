import pulp

# Given data
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

# Create the linear programming problem
problem = pulp.LpProblem("Ad_Clicks_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=0, cat='Continuous')
for a in range(A):
    x[a].upBound = data['max_clicks'][a]

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Requirement"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Requirement"
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Requirement"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Requirement"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')