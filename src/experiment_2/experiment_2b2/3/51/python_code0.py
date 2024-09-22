import pulp

# Data input
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

# Unpack data
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
A = len(young_clicks)

# Initialize the problem
problem = pulp.LpProblem("MaximizeUniqueClicks", pulp.LpMaximize)

# Decision variables: Number of clicks purchased for each ad type
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function: Maximize total unique clicks
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A))

# Constraints
# Budget constraint
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget

# Goal constraints for age groups
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old

# Solve the problem
problem.solve()

# Prepare output
clicks_purchased = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_purchased,
    "total_unique_clicks": total_unique_clicks
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')