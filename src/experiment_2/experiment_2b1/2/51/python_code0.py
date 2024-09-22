import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 
        'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 
        'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 
        'budget': 105000}

# Extract data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective function: Maximize unique clicks
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Collecting results
result_clicks = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

# Output results
output = {
    "clicks": result_clicks,
    "total_unique_clicks": total_unique_clicks
}

print(f' (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')