import pulp
import json

# Load data in JSON format
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}')

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
A = len(costs)  # Number of ad types

# Create the linear programming problem
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Objective function
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += (pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint")
problem += (pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint")
for a in range(A):
    problem += (clicks[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a + 1}")

# Solve the problem
problem.solve()

# Print the results
for a in range(A):
    print(f"Clicks for ad type {a + 1}: {clicks[a].varValue} (thousands)")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')