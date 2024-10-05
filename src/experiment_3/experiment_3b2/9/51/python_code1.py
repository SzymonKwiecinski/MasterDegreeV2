import pulp
import json

# Data from the provided JSON
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

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
budget = data['budget']
A = len(young_clicks)  # Number of ad types

# Create the problem variable
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=None, cat='Continuous')
for a in range(A):
    x[a].upBound = max_clicks[a]  # Set individual upper bounds

# Objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Age Group Click Goals
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Goal"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Goal"

# Unique Clicks Goals
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Goal"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Goal"

# Budget Constraint
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Print the results
for a in range(A):
    print(f"Clicks purchased for ad type {a + 1}: {x[a].varValue} (in thousands)")
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')