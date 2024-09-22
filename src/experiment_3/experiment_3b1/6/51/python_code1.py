import pulp
import json

# Input data
data_json = '''{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}'''
data = json.loads(data_json)

# Extract values
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

# Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Define decision variables
A = len(young_clicks)
x = [pulp.LpVariable(f'x_{a+1}', lowBound=0, upBound=max_clicks[a]) for a in range(A)]

# Define the objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Define the constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Goal_Young_Clicks"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Goal_Old_Clicks"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Goal_Unique_Old_Clicks"
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Output results
clicks = [pulp.value(x[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks: {clicks}')
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')