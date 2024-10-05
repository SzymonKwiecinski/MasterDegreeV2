import pulp
import json

# Data
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90]}')

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

# Number of alternatives
A = len(costs)

# Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0)

# Objective Function
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum(young_clicks[a] * unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Requirement"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}"

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')