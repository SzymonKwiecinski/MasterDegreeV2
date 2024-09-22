import pulp
import json

# Input data
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
A = len(costs)  # Number of ad types

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Problem Definition
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Visitor_Clicks"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Visitor_Clicks"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Visitor_Clicks"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Visitor_Clicks"

for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output
for a in range(A):
    print(f'Clicks for ad type {a + 1} (in thousands): {clicks[a].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')