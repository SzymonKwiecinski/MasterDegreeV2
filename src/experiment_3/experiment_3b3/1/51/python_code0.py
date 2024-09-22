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

# Problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, cat='Continuous') for a in range(A)]

# Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# 1. Total clicks from young visitors
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young"

# 2. Total clicks from older visitors
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old"

# 3. Total unique clicks from young visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

# 4. Total unique clicks from older visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# 5. Total cost must not exceed the budget
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget"

# 6. Maximum clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a+1}"

# Solve
problem.solve()

# Output
for a in range(A):
    print(f"Clicks for ad type {a+1} (in thousands): {x[a].varValue}")

print(f"Total unique clicks (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")