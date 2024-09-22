import pulp
import json

# Data in JSON format
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

# Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
budget = data['budget']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

# Number of ad types
A = len(young_clicks)

# Create the problem
problem = pulp.LpProblem("Ad_Clicks_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=None)

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum(x[a] for a in range(A)) <= budget, "Budget_Constraint"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Output results
for a in range(A):
    print(f'Clicks purchased for ad type {a+1}: {x[a].varValue} (in thousands)')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')