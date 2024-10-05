import pulp
import json

# Given data in JSON format
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

# Extract data from the JSON
goal_young = data['goal_young']
goal_old = data['goal_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

# Number of alternatives
A = len(unique_clicks)

# Create the problem variable
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=[max_clicks[a] for a in range(A)], cat='Continuous')

# Objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum((young_clicks[a] / 100) * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum((old_clicks[a] / 100) * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')