import pulp
import json

# Data from JSON format
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

# Parameters
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

# Define the problem
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young + goal_unique_old, "Total_Unique_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Output results
clicks = [x[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks: {clicks}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')