import pulp
import json

# Input data in JSON format
data_json = '{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}'
data = json.loads(data_json)

# Problem setup
A = len(data['young_clicks'])  # Number of ad types
problem = pulp.LpProblem("Online_Advertising_Campaign", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=None)

# Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total Cost"

# Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Visitors"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Visitors"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

# Maximum clicks limitation for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_Ad_{a+1}"

# Solve the problem
problem.solve()

# Output results
clicks = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f'Clicks: {clicks}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')