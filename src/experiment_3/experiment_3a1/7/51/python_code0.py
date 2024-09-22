import pulp
import json

# Data
data_json = '{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}'
data = json.loads(data_json)

# Parameters
A = len(data['young_clicks'])
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
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Click_Constraint"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Click_Constraint"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Click_Constraint"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Click_Constraint"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a+1}"

# Solve the problem
problem.solve()

# Output results
clicks = [x[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks Purchased: {clicks}')
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')