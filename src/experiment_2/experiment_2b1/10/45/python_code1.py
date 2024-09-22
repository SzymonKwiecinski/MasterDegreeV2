import pulp
import json

# Given data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 
        'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}

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

# Number of ad types
A = len(young_clicks)

# Create the problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]), "Total_Cost"

# Constraints
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Requirement"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Requirement"

# Setting max clicks constraints
for a in range(A):
    problem += clicks[a] <= max_clicks[a], f"Max_Clicks_{a}"

# Solve the problem
problem.solve()

# Prepare the output
clicks_values = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

# Print the results
output = {
    "clicks": clicks_values,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')