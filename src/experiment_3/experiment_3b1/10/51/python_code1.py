import pulp
import json

# Load data
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

# Parameters
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

# Create the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision Variables
A = len(young_clicks)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Print results
clicks_requested = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks Requested: {clicks_requested}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')