import pulp
import json

# Data provided in JSON format
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

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

# Number of ad types
A = len(young_clicks)

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
click = pulp.LpVariable.dicts("click", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * click[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(young_clicks[a] * click[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * click[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * click[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * click[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * click[a] for a in range(A)) <= budget, "Budget_Constraint"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'click_{a}: {click[a].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')