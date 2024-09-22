import pulp
import json

# Data from the provided JSON format
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}")

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

# Number of ad types
A = len(costs)

# Problem definition
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Min_Young_Visitors"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Min_Old_Visitors"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Min_Unique_Young_Visitors"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Min_Unique_Old_Visitors"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_{a+1}"

# Solve the problem
problem.solve()

# Output results
clicks = [x[a].varValue for a in range(A)]
total_cost = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print(f' (Clicks): <CLICKS>{clicks}</CLICKS>')