import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

# Extracting the data
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

A = len(young_clicks)

# Setting up the Linear Programming problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Goal_Young_Clicks"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Goal_Old_Clicks"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young + goal_unique_old, "Goal_Unique_Clicks"

for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_Ad_{a}"

# Solve the problem
problem.solve()

# Retrieve results
clicks_values = [clicks[a].varValue for a in range(A)]
total_unique_clicks = sum(unique_clicks[a] * clicks_values[a] for a in range(A))

# Output the results
result = {
    "clicks": clicks_values,
    "total_unique_clicks": total_unique_clicks
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')