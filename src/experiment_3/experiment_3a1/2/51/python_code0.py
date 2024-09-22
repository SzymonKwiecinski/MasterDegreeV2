import pulp
import json

# Data input
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

# Number of ad types
A = len(costs)

# Create the model
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None)

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
# Total budget constraint
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

# Young clicks constraint
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"

# Old clicks constraint
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"

# Unique clicks constraints for the young demographic
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Clicks_Young_Constraint"

# Unique clicks constraints for the old demographic
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Clicks_Old_Constraint"

# Maximum clicks constraint
for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_Constraint_{a}"

# Solve the problem
problem.solve()

# Output the results
for a in range(A):
    print(f'Clicks purchased for ad type {a+1}: {clicks[a].varValue} (in thousands)')

total_unique_clicks = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')