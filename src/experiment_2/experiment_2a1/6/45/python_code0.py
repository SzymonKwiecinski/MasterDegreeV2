import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

# Extracting data from the input
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

# Create the problem
problem = pulp.LpProblem("Ad_Campaign_Optimization", pulp.LpMinimize)

# Decision variables: clicks for each ad type (in thousands)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[mc/1000 for mc in max_clicks], cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints for goals
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Youth_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Requirement"

# Constraints for unique clicks
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Youth_Clicks_Requirement"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Requirement"

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(problem.objective)
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')