import pulp
import json

# Input data in JSON format
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Number of ad types
A = len(young_clicks)

# Decision variables: clicks purchased for each ad type (in thousands)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function: maximize total unique clicks
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(clicks[a] for a in range(A)) >= goal_unique_young + goal_unique_old, "Total_Unique_Clicks_Constraint"

# Individual maximum clicks constraints
for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}"

# Solve the problem
problem.solve()

# Prepare the output
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Create output in the required format
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

# Print Output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')