import json
import pulp

# Corrected input data to use double quotes for JSON
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

# Extract data from JSON
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

# Number of ad types
A = len(young_clicks)

# Create the LP problem
problem = pulp.LpProblem('Maximize_Unique_Clicks', pulp.LpMaximize)

# Decision variables
clicks = pulp.LpVariable.dicts('clicks', range(A), lowBound=0, upBound=[max_clicks[i] for i in range(A)], cat='Continuous')

# Objective function: maximize total unique clicks
problem += pulp.lpSum([unique_clicks[i] * clicks[i] for i in range(A)])

# Constraints
problem += pulp.lpSum([costs[i] * clicks[i] for i in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([young_clicks[i] * clicks[i] for i in range(A)]) >= goal_young, "Goal_Young_Clicks"
problem += pulp.lpSum([old_clicks[i] * clicks[i] for i in range(A)]) >= goal_old, "Goal_Old_Clicks"
problem += pulp.lpSum([unique_clicks[i] * clicks[i] for i in range(A)]) >= goal_unique_young + goal_unique_old, "Goal_Unique_Clicks"

# Solve the problem
problem.solve()

# Collect results
total_unique_clicks = pulp.value(problem.objective)
clicks_result = [clicks[i].varValue for i in range(A)]

# Output the results
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')