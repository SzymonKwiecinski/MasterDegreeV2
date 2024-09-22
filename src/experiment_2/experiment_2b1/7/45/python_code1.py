import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90]}

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

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
clicks = pulp.LpVariable.dicts("click", range(A), lowBound=0, upBound=None, cat='Continuous')

# Objective function
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)), "Total_Cost"

# Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Click_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Click_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Click_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Click_Constraint"

# Set the upper bounds for each decision variable
for a in range(A):
    clicks[a].upBound = max_clicks[a] / 1000  # Convert back to actual clicks from thousands

# Solve the problem
problem.solve()

# Output results
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')