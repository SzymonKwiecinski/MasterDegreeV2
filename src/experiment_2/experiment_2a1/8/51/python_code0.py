import pulp
import json

# Input data
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 
        'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 
        'unique_clicks': [40, 75, 90], 'budget': 105000}

# Variables
A = len(data['young_clicks'])
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

# Objective function: Maximize total unique clicks
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum([costs[a] * clicks[a] for a in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([young_clicks[a] * clicks[a] for a in range(A)]) >= goal_young, "Young_Click_Constraint"
problem += pulp.lpSum([old_clicks[a] * clicks[a] for a in range(A)]) >= goal_old, "Old_Click_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_young, "Unique_Young_Click_Constraint"
problem += pulp.lpSum([unique_clicks[a] * clicks[a] for a in range(A)]) >= goal_unique_old, "Unique_Old_Click_Constraint"

# Solve the problem
problem.solve()

# Results
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')