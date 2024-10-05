import pulp
import json

# Data provided in JSON format
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}')

# Extracting data from the JSON
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

# Define the problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0)

# Objective Function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Goal_Young_Clicks"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Goal_Old_Clicks"
problem += pulp.lpSum(unique_clicks[a] * young_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(unique_clicks[a] * old_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Goal_Unique_Old_Clicks"

# Constraints for max clicks
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_Ad_{a+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')