import pulp
import json

# Input data
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}')

# Problem variables
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

A = len(young_clicks)

# Problem definition
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective function
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old

# Solve the problem
problem.solve()

# Output results
clicks_values = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

result = {
    "clicks": clicks_values,
    "total_cost": total_cost
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')