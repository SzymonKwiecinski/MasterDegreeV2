import pulp
import json

# Input data in JSON format
data = '{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}'
input_data = json.loads(data)

# Extracting data from input
goal_young = input_data['goal_young']
goal_old = input_data['goal_old']
goal_unique_young = input_data['goal_unique_young']
goal_unique_old = input_data['goal_unique_old']
young_clicks = input_data['young_clicks']
old_clicks = input_data['old_clicks']
costs = input_data['costs']
max_clicks = input_data['max_clicks']
unique_clicks = input_data['unique_clicks']
budget = input_data['budget']

# Number of ad types
A = len(young_clicks)

# Create a linear programming problem
problem = pulp.LpProblem("Ad_Campaign_Optimization", pulp.LpMaximize)

# Decision variables: clicks_a
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function: maximize total unique clicks
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum(unique_clicks[a] * young_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks"
problem += pulp.lpSum(unique_clicks[a] * old_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks"

# Solve the problem
problem.solve()

# Extracting results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output the results
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

# Print the output
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')