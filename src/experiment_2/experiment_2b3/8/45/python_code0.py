import pulp

# Parse the input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}

# Extract data
goal_young = data["goal_young"]
goal_old = data["goal_old"]
goal_unique_young = data["goal_unique_young"]
goal_unique_old = data["goal_unique_old"]
young_clicks = data["young_clicks"]
old_clicks = data["old_clicks"]
costs = data["costs"]
max_clicks = data["max_clicks"]
unique_clicks = data["unique_clicks"]
A = len(young_clicks)

# Initialize the problem
problem = pulp.LpProblem("Advertising_Campaign_Minimization", pulp.LpMinimize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints for demographic click goals
problem += pulp.lpSum([young_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_young, "YoungClicksGoal"
problem += pulp.lpSum([old_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_old, "OldClicksGoal"

# Constraints for unique click goals
problem += pulp.lpSum([unique_clicks[a] * clicks[a] / 100 for a in range(A)]) >= goal_unique_young + goal_unique_old, "UniqueClicksGoal"
problem += pulp.lpSum([(young_clicks[a] / 100) * (unique_clicks[a] / 100) * clicks[a] for a in range(A)]) >= goal_unique_young, "UniqueYoungClicksGoal"
problem += pulp.lpSum([(old_clicks[a] / 100) * (unique_clicks[a] / 100) * clicks[a] for a in range(A)]) >= goal_unique_old, "UniqueOldClicksGoal"

# Solve the problem
problem.solve()

# Prepare the output
click_values = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": click_values,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')