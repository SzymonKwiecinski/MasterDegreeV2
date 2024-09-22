import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}

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

# Number of ad types
A = len(young_clicks)

# Create the Linear Programming problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

# Decision variables: clicks_a for each ad type a
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective Function: Minimize total cost
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)])

# Constraints
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young, "Young_Clicks_Goal"
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old, "Old_Clicks_Goal"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Goal"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Goal"

# Solve the problem
problem.solve()

# Extract results
clicks_result = [clicks[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')