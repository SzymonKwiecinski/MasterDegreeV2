import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300,
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120],
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

# Extract data from JSON
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

# Number of ad types
A = len(young_clicks)

# Define the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Define decision variables
clicks = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective function: maximize total unique clicks
total_unique_clicks = pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)])
problem += total_unique_clicks, "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum([clicks[a] * costs[a] for a in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([clicks[a] * young_clicks[a] / 1000 for a in range(A)]) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * old_clicks[a] / 1000 for a in range(A)]) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Prepare output
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks_result = pulp.value(problem.objective)

# Output the results
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')