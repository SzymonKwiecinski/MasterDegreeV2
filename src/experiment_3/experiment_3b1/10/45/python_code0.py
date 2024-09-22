import pulp
import json

# Data in JSON format
data_json = '{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}'
data = json.loads(data_json)

# Parameters
A = len(data['young_clicks'])
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

# Create the linear programming problem
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Objective function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += (pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint")
problem += (pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint")
problem += (pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint")
for a in range(A):
    problem += (x[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}")

# Solve the problem
problem.solve()

# Output the results
clicks_purchased = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks purchased for each ad type (in thousands): {clicks_purchased}')
print(f'Total cost of the ad campaign (Objective Value): <OBJ>{total_cost}</OBJ>')