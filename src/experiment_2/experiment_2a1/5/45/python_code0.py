import pulp
import json

# Input data
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

# Problem definition
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=[max_clicks[i] for i in range(A)], cat='Continuous')

# Objective function
problem += pulp.lpSum([costs[i] * clicks[i] for i in range(A)]), "Total_Cost"

# Constraints
problem += pulp.lpSum([young_clicks[i] * clicks[i] for i in range(A)]) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum([old_clicks[i] * clicks[i] for i in range(A)]) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum([unique_clicks[i] * clicks[i] for i in range(A)]) >= goal_unique_young, "Young_Unique_Clicks_Requirement"
problem += pulp.lpSum([unique_clicks[i] * clicks[i] for i in range(A)]) >= goal_unique_old, "Old_Unique_Clicks_Requirement"

# Solve the problem
problem.solve()

# Prepare output
clicks_result = [clicks[i].varValue for i in range(A)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')