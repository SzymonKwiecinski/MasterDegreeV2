import pulp
import json

# Input data
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

# Extracting parameters from the data
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

# Defining the Linear Programming problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

# Objective function: Maximize total unique clicks
total_unique_clicks = pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)])
problem += total_unique_clicks

# Constraints
problem += pulp.lpSum([clicks[a] * costs[a] for a in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Output results
result_clicks = [clicks[a].varValue for a in range(A)]
total_unique_clicks_value = pulp.value(total_unique_clicks)

output = {
    "clicks": result_clicks,
    "total_unique_clicks": total_unique_clicks_value
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')