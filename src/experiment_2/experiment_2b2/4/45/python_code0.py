import pulp

# Input Data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90]
}

# Extracting data
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

# Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Objective
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints
problem += pulp.lpSum([young_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_young
problem += pulp.lpSum([old_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_old
problem += pulp.lpSum([unique_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_unique_young
problem += pulp.lpSum([unique_clicks[a] / 100 * clicks[a] for a in range(A)]) >= goal_unique_old

# Solve
problem.solve()

# Result
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

import json
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')