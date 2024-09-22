import pulp

# Data from the input
data = {
    "goal_young": 500,
    "goal_old": 600,
    "goal_unique_young": 250,
    "goal_unique_old": 300,
    "young_clicks": [40, 30, 70],
    "old_clicks": [60, 70, 30],
    "costs": [75, 100, 120],
    "max_clicks": [600, 300, 300],
    "unique_clicks": [40, 75, 90]
}

# Constants
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

# Number of ad types
A = len(young_clicks)

# Define the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables: number of clicks to purchase for each ad type
clicks = [pulp.LpVariable(f"clicks_{i}", lowBound=0, upBound=max_clicks[i], cat='Continuous') for i in range(A)]

# Objective function: Minimize total cost
problem += pulp.lpSum([costs[i] * clicks[i] for i in range(A)])

# Constraints
# 1. Total clicks from young visitors
problem += pulp.lpSum([young_clicks[i] * clicks[i] for i in range(A)]) >= goal_young

# 2. Total clicks from old visitors
problem += pulp.lpSum([old_clicks[i] * clicks[i] for i in range(A)]) >= goal_old

# 3. Total unique clicks from young visitors
problem += pulp.lpSum([unique_clicks[i] * clicks[i] * (young_clicks[i] / 100) for i in range(A)]) >= goal_unique_young

# 4. Total unique clicks from old visitors
problem += pulp.lpSum([unique_clicks[i] * clicks[i] * (old_clicks[i] / 100) for i in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "clicks": [pulp.value(clicks[i]) for i in range(A)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")