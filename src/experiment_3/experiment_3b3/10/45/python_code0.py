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
A = len(data['costs'])

# Problem
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0, cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
# Young Visitors Clicks
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young"

# Old Visitors Clicks
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old"

# Unique Clicks from Young Visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

# Unique Clicks from Old Visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# Maximum Allowable Clicks
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Click_{a}"

# Solve Problem
problem.solve()

# Output Results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

# Optional: To see the purchased clicks for each ad type
for a in range(A):
    print(f"Clicks purchased for ad type {a+1}: {x[a].varValue} (in thousands)")